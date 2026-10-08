function Get-ClaudeTranscriptReview {
    param([string] $TranscriptPath, [string] $Prompt)

    $matched = $false
    $lastResult = $null
    if (-not (Test-Path -LiteralPath $TranscriptPath -PathType Leaf)) {
        return [pscustomobject]@{ Matched = $false; Result = $null }
    }
    foreach ($line in [IO.File]::ReadLines($TranscriptPath)) {
        try { $entry = $line | ConvertFrom-Json } catch { continue }
        if ($entry.type -eq 'user' -and $entry.message.content -is [string] -and
            -not $entry.isCompactSummary) {
            $matched = $entry.message.content -ceq $Prompt
            $lastResult = $null
        } elseif ($matched -and $entry.type -eq 'assistant' -and
                  $entry.message.stop_reason -eq 'end_turn') {
            $textBlocks = @($entry.message.content | Where-Object { $_.type -eq 'text' })
            if ($textBlocks.Count -gt 0) {
                $lastResult = ($textBlocks | ForEach-Object { $_.text }) -join "`n"
            }
        }
    }
    return [pscustomobject]@{ Matched = $matched; Result = $lastResult }
}
