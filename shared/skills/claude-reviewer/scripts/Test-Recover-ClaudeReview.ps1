$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Recover-ClaudeReview.ps1')

$path = Join-Path ([IO.Path]::GetTempPath()) ("claude-review-test-" + [guid]::NewGuid().ToString() + ".jsonl")
try {
    $prompt = 'Review exact head abc123'
    $user = @{ type = 'user'; message = @{ content = $prompt } } | ConvertTo-Json -Compress -Depth 5
    $final = @{ type = 'assistant'; message = @{ stop_reason = 'end_turn'; content = @(@{ type = 'text'; text = 'No blocker' }) } } | ConvertTo-Json -Compress -Depth 5
    [IO.File]::WriteAllLines($path, @($user), (New-Object Text.UTF8Encoding($false)))
    $pending = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $prompt
    if (-not $pending.Matched -or $pending.Result) { throw 'pending review was misclassified' }

    [IO.File]::WriteAllLines($path, @($user, $final), (New-Object Text.UTF8Encoding($false)))
    $recovered = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $prompt
    if (-not $recovered.Matched -or $recovered.Result -ne 'No blocker') { throw 'completed review was not recovered' }

    $later = @{ type = 'user'; message = @{ content = 'Review another head' } } | ConvertTo-Json -Compress -Depth 5
    [IO.File]::WriteAllLines($path, @($user, $final, $later), (New-Object Text.UTF8Encoding($false)))
    $superseded = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $prompt
    if ($superseded.Matched -or $superseded.Result) { throw 'later prompt was ignored' }
    'Reviewer transcript recovery passed'
} finally {
    Remove-Item -LiteralPath $path -ErrorAction SilentlyContinue
}
