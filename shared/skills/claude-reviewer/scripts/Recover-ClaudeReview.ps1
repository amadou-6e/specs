function Get-ClaudeTranscriptReview {
    param([string] $TranscriptPath, [string] $Prompt, [long] $StartOffset = 0)

    $matched = $false
    $resultParts = New-Object 'System.Collections.Generic.List[string]'
    if (-not (Test-Path -LiteralPath $TranscriptPath -PathType Leaf)) {
        return [pscustomobject]@{ Matched = $false; Result = $null }
    }
    $stream = [IO.File]::Open($TranscriptPath, [IO.FileMode]::Open,
                             [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        if ($StartOffset -gt $stream.Length) {
            return [pscustomobject]@{ Matched = $false; Result = $null }
        }
        $stream.Seek($StartOffset, [IO.SeekOrigin]::Begin) | Out-Null
        $reader = New-Object IO.StreamReader($stream, (New-Object Text.UTF8Encoding($false)))
        try {
            while (($line = $reader.ReadLine()) -ne $null) {
                try { $entry = $line | ConvertFrom-Json } catch { continue }
                if ($entry.type -eq 'user' -and -not $entry.isCompactSummary) {
                    $content = $entry.message.content
                    $userText = if ($content -is [string]) { $content } else {
                        (@($content | Where-Object { $_.type -eq 'text' } |
                            ForEach-Object { $_.text })) -join "`n"
                    }
                    if ($userText) {
                        $matched = ($userText -replace "`r`n", "`n").TrimEnd("`r", "`n") -ceq
                                   ($Prompt -replace "`r`n", "`n").TrimEnd("`r", "`n")
                        $resultParts.Clear()
                    }
                } elseif ($matched -and $entry.type -eq 'assistant' -and
                          $entry.message.stop_reason -eq 'end_turn' -and
                          -not $entry.isApiErrorMessage -and
                          -not $entry.message.isApiErrorMessage -and
                          $entry.message.model -ne '<synthetic>') {
                    foreach ($block in @($entry.message.content | Where-Object { $_.type -eq 'text' })) {
                        $resultParts.Add($block.text)
                    }
                }
            }
        } finally {
            $reader.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
    $result = if ($resultParts.Count) { $resultParts -join "`n" } else { $null }
    return [pscustomobject]@{ Matched = $matched; Result = $result }
}
