[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string] $WorkspaceRoot,
    [Parameter(Mandatory = $true)] [string] $StateDirectory,
    [Parameter(Mandatory = $true)] [string] $PromptFile,
    [string] $ResolvePendingSha256,
    [string] $CodexSessionId = $env:CODEX_SESSION_ID,
    [ValidateRange(30, 1800)] [int] $TimeoutSeconds = 180
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Recover-ClaudeReview.ps1')

if (-not $CodexSessionId) {
    throw 'CODEX_SESSION_ID is unavailable. Pass -CodexSessionId to bind the reviewer to a stable Codex conversation.'
}
$codexId = [guid]::Parse($CodexSessionId).ToString()
$workspace = [IO.Path]::GetFullPath($WorkspaceRoot).TrimEnd('\', '/')
$state = [IO.Path]::GetFullPath($StateDirectory).TrimEnd('\', '/')
$promptPath = [IO.Path]::GetFullPath($PromptFile)
$withinWorkspace = $state.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
if (-not $withinWorkspace) {
    throw 'The reviewer state directory must be inside the trusted workspace.'
}
if (-not (Test-Path -LiteralPath $promptPath -PathType Leaf)) {
    throw 'The reviewer prompt file does not exist.'
}
$promptWithinWorkspace = $promptPath.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
if (-not $promptWithinWorkspace) {
    throw 'The reviewer prompt file must be inside the trusted workspace.'
}

& git -C $workspace check-ignore -q -- $state
if ($LASTEXITCODE -ne 0) {
    throw 'The reviewer state directory must be ignored by Git before a session is created.'
}
& git -C $workspace check-ignore -q -- $promptPath
if ($LASTEXITCODE -ne 0) {
    throw 'The reviewer prompt file must be ignored by Git.'
}

if ($env:ANTHROPIC_API_KEY -or $env:ANTHROPIC_AUTH_TOKEN -or
    $env:CLAUDE_CODE_OAUTH_TOKEN -or $env:ANTHROPIC_BASE_URL -or
    $env:CLAUDE_CONFIG_DIR -or
    $env:CLAUDE_CODE_USE_BEDROCK -or $env:CLAUDE_CODE_USE_VERTEX -or
    $env:CLAUDE_CODE_USE_FOUNDRY) {
    throw 'A provider override is present. Use the existing Claude subscription login for this reviewer.'
}

$extensionRoot = Join-Path $env:USERPROFILE '.vscode\extensions'
$candidates = @(Get-ChildItem -LiteralPath $extensionRoot -Directory -Filter 'anthropic.claude-code-*-win32-x64' -ErrorAction SilentlyContinue |
    ForEach-Object {
        $exe = Join-Path $_.FullName 'resources\native-binary\claude.exe'
        if (Test-Path -LiteralPath $exe -PathType Leaf) {
            [pscustomobject]@{ Path = $exe; Version = [version]([regex]::Match($_.Name, 'claude-code-(\d+\.\d+\.\d+)').Groups[1].Value) }
        }
    } | Sort-Object Version -Descending)
if ($candidates.Count -eq 0) {
    throw 'No Claude Code VS Code executable was found. Install Claude Code or update the launcher discovery in this skill.'
}
$claude = $candidates[0].Path

$authJson = & $claude auth status
if ($LASTEXITCODE -ne 0) {
    throw 'Claude Code authentication status could not be checked.'
}
$auth = ($authJson -join "`n") | ConvertFrom-Json
if (-not $auth.loggedIn -or $auth.authMethod -ne 'claude.ai') {
    throw 'The existing Claude subscription login is unavailable. Sign in once under the normal OS user profile.'
}

New-Item -ItemType Directory -Path $state -Force | Out-Null
$recordPath = Join-Path $state "$codexId.json"
$lockPath = Join-Path $state "$codexId.lock"
$lock = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::Write, [IO.FileShare]::None)
try {
    $recordExists = Test-Path -LiteralPath $recordPath -PathType Leaf
    if ($recordExists) {
        $record = Get-Content -LiteralPath $recordPath -Raw | ConvertFrom-Json
        $claudeId = [guid]::Parse($record.claude_session_id).ToString()
        if (-not $record.PSObject.Properties['initialized']) {
            $record | Add-Member -NotePropertyName initialized -NotePropertyValue $true
        }
        if (-not $record.PSObject.Properties['pending_prompt_sha256']) {
            $record | Add-Member -NotePropertyName pending_prompt_sha256 -NotePropertyValue $null
        }
        if (-not $record.PSObject.Properties['pending_transcript_length']) {
            $record | Add-Member -NotePropertyName pending_transcript_length -NotePropertyValue $null
        }
    } else {
        $claudeId = [guid]::NewGuid().ToString()
        $record = [pscustomobject]@{ codex_session_id = $codexId; claude_session_id = $claudeId; initialized = $false; pending_prompt_sha256 = $null; pending_transcript_length = $null }
        $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
    }
    if ($record.codex_session_id -ne $codexId) {
        throw 'The reviewer ledger belongs to a different Codex session.'
    }
    $resume = [bool]$record.initialized
    $projectsDirectory = Join-Path $env:USERPROFILE '.claude\projects'
    if (-not $resume -and (Test-Path -LiteralPath $projectsDirectory)) {
        $resume = @(Get-ChildItem -LiteralPath $projectsDirectory -File -Recurse -Filter "$claudeId.jsonl" -ErrorAction SilentlyContinue).Count -gt 0
    }

    $arguments = @(
        '--print', '--output-format', 'json', '--safe-mode', '--restricted',
        '--effort', 'low',
        '--tools', 'Read,Glob,Grep', '--permission-mode', 'dontAsk',
        '--permission-prompts', 'none', '--strict-mcp-config'
    )
    if ($resume) {
        $arguments += @('--resume', $claudeId)
    } else {
        $arguments += @('--session-id', $claudeId)
    }

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $claude
    $startInfo.Arguments = $arguments -join ' '
    $startInfo.WorkingDirectory = $workspace
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardInput = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    # Keep long-lived reviewer conversations compact without changing the
    # user's interactive Claude sessions or global settings.
    $startInfo.EnvironmentVariables['CLAUDE_AUTOCOMPACT_PCT_OVERRIDE'] = '60'
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $startInfo.StandardOutputEncoding = $utf8
    $startInfo.StandardErrorEncoding = $utf8
    $promptBytes = [IO.File]::ReadAllBytes($promptPath)
    if ($promptBytes.Length -ge 3 -and $promptBytes[0] -eq 0xEF -and
        $promptBytes[1] -eq 0xBB -and $promptBytes[2] -eq 0xBF) {
        $withoutBom = New-Object byte[] ($promptBytes.Length - 3)
        [Array]::Copy($promptBytes, 3, $withoutBom, 0, $withoutBom.Length)
        $promptBytes = $withoutBom
    }
    if ($promptBytes.Length -eq 0) { throw 'The reviewer prompt file is empty.' }
    $promptText = $utf8.GetString($promptBytes)
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $promptHash = [BitConverter]::ToString($sha.ComputeHash($promptBytes)).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
    if ($record.pending_prompt_sha256) {
        if ($ResolvePendingSha256) {
            if ($ResolvePendingSha256 -ne $record.pending_prompt_sha256) {
                throw 'The supplied pending digest does not match the unresolved review.'
            }
            $record.pending_prompt_sha256 = $null
            $record.pending_transcript_length = $null
            $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
        } else {
        if ($record.pending_prompt_sha256 -ne $promptHash) {
            throw "A prior reviewer request is unresolved ($($record.pending_prompt_sha256)). Inspect its transcript before explicitly resolving it."
        }
        $transcripts = @(Get-ChildItem -LiteralPath $projectsDirectory -File -Recurse -Filter "$claudeId.jsonl" -ErrorAction SilentlyContinue)
        if ($transcripts.Count -gt 1) { throw 'Multiple reviewer transcripts match the same session; recovery requires inspection.' }
        $recovery = if ($transcripts.Count -eq 1) {
            Get-ClaudeTranscriptReview -TranscriptPath $transcripts[0].FullName -Prompt $promptText -StartOffset ([long]$record.pending_transcript_length)
        } else { $null }
        if (-not $recovery -or -not $recovery.Matched -or -not $recovery.Result) {
            throw "The identical reviewer request is uncertain ($promptHash). Refusing a duplicate submission. Inspect the transcript, then use -ResolvePendingSha256 with this digest only if a new request is warranted."
        }
        $record.pending_prompt_sha256 = $null
        $record.pending_transcript_length = $null
        $record.initialized = $true
        $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
        [Console]::OutputEncoding = $utf8
        Write-Output ([pscustomobject]@{ type = 'result'; subtype = 'recovered'; is_error = $false; session_id = $claudeId; result = $recovery.Result } | ConvertTo-Json -Compress -Depth 5)
        return
        }
    } elseif ($ResolvePendingSha256) {
        throw 'No pending reviewer request exists for the supplied digest.'
    }
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    $transcripts = @(Get-ChildItem -LiteralPath $projectsDirectory -File -Recurse -Filter "$claudeId.jsonl" -ErrorAction SilentlyContinue)
    if ($transcripts.Count -gt 1) { throw 'Multiple reviewer transcripts match the same session.' }
    $record.pending_prompt_sha256 = $promptHash
    $record.pending_transcript_length = if ($transcripts.Count -eq 1) { [long]$transcripts[0].Length } else { [long]0 }
    $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
    $started = $false
    try {
        if (-not $process.Start()) {
            throw 'Claude Code did not start.'
        }
        $started = $true
        $outputTask = $process.StandardOutput.ReadToEndAsync()
        $errorTask = $process.StandardError.ReadToEndAsync()
        $inputFailed = $false
        try {
            $process.StandardInput.BaseStream.Write($promptBytes, 0, $promptBytes.Length)
        } catch [IO.IOException] {
            $inputFailed = $true
        } finally {
            $process.StandardInput.Close()
        }
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            if (-not $process.HasExited) {
                try { $process.Kill() } catch [InvalidOperationException] {
                    if (-not $process.HasExited) { throw }
                }
            }
            $process.WaitForExit(5000) | Out-Null
            throw "Claude Code review exceeded $TimeoutSeconds seconds. The Claude session ID is retained; its transcript may contain a partial turn."
        }
        if (-not $outputTask.Wait(5000) -or -not $errorTask.Wait(5000)) {
            throw 'Claude Code exited but an output pipe remained open. The reviewer session ID is retained.'
        }
        $nativeDiagnostic = 'native_error'
        $nativeError = $errorTask.Result
        if ($nativeError -match 'already (in use|exists)|session.?id.*(used|exists)') {
            $nativeDiagnostic = 'session_id_conflict'
        } elseif ($nativeError -match 'auth|login|credential') {
            $nativeDiagnostic = 'authentication_error'
        } elseif ($nativeError -match 'network|connect|timeout|ENET|ECONN') {
            $nativeDiagnostic = 'network_error'
        } elseif ($nativeError -match 'unknown option|invalid argument|unrecognized') {
            $nativeDiagnostic = 'cli_argument_error'
        }
        if ($process.ExitCode -ne 0) {
            throw "Claude Code review exited with code $($process.ExitCode) ($nativeDiagnostic). The Claude session ID is retained; its transcript may contain a partial turn."
        }
        if ($inputFailed) {
            throw 'Claude Code exited before consuming the review prompt. The reviewer session ID is retained.'
        }
        $json = $outputTask.Result
    } catch {
        if (-not $started) {
            $record.pending_prompt_sha256 = $null
            $record.pending_transcript_length = $null
            $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
        }
        throw
    } finally {
        $process.Dispose()
    }
    $result = $json | ConvertFrom-Json
    if ($result.is_error) {
        throw 'Claude Code returned an error result. The Claude session ID is retained; its transcript may contain a partial turn.'
    }
    if (-not $result.session_id -or $result.session_id -ne $claudeId) {
        throw 'Claude Code returned an unexpected session ID; refusing to change the reviewer binding.'
    }
    $record.initialized = $true
    $record.pending_prompt_sha256 = $null
    $record.pending_transcript_length = $null
    $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $recordPath -Encoding UTF8
    [Console]::OutputEncoding = $utf8
    Write-Output $json
} finally {
    $lock.Dispose()
}
