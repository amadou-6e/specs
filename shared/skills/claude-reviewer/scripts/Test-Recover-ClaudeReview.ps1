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

    # A prior answer must not be recovered for a new, unanswered identical turn.
    [IO.File]::WriteAllLines($path, @($user, $final), (New-Object Text.UTF8Encoding($false)))
    $offset = (Get-Item -LiteralPath $path).Length
    [IO.File]::WriteAllLines($path, @($user, $final, $user), (New-Object Text.UTF8Encoding($false)))
    $newPending = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $prompt -StartOffset $offset
    if (-not $newPending.Matched -or $newPending.Result) { throw 'older answer was reused' }

    $synthetic = @{ type = 'assistant'; isApiErrorMessage = $true; message = @{
        model = '<synthetic>'; stop_reason = 'end_turn';
        content = @(@{ type = 'text'; text = 'usage limit' })
    } } | ConvertTo-Json -Compress -Depth 5
    [IO.File]::WriteAllLines($path, @($user, $final, $user, $synthetic),
                            (New-Object Text.UTF8Encoding($false)))
    $errorResult = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $prompt -StartOffset $offset
    if (-not $errorResult.Matched -or $errorResult.Result) { throw 'synthetic error was recovered' }

    $crlfPrompt = "Review`r`nhead"
    $blockUser = @{ type = 'user'; message = @{ content = @(
        @{ type = 'text'; text = "Review`nhead" }) } } | ConvertTo-Json -Compress -Depth 5
    $toolResult = @{ type = 'user'; message = @{ content = @(
        @{ type = 'tool_result'; content = 'read only' }) } } | ConvertTo-Json -Compress -Depth 5
    $summary = @{ type = 'user'; isCompactSummary = $true; message = @{
        content = 'compact summary' } } | ConvertTo-Json -Compress -Depth 5
    $splitFinal = @{ type = 'assistant'; message = @{ stop_reason = 'end_turn';
        content = @(@{ type = 'text'; text = 'First' }, @{ type = 'text'; text = 'second' }) } } |
        ConvertTo-Json -Compress -Depth 5
    [IO.File]::WriteAllLines($path, @($blockUser, $toolResult, $summary, $splitFinal),
                            (New-Object Text.UTF8Encoding($false)))
    $blocks = Get-ClaudeTranscriptReview -TranscriptPath $path -Prompt $crlfPrompt
    if (-not $blocks.Matched -or $blocks.Result -ne "First`nsecond") {
        throw 'real-shape blocks were not recovered'
    }
    'Reviewer transcript recovery passed'
} finally {
    Remove-Item -LiteralPath $path -ErrorAction SilentlyContinue
}
