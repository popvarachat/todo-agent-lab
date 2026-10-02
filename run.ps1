$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Todo Agent Lab"
Write-Host "1) Sync Planner"
python .\scripts\sync_planner.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "2) Analyze Use Cases"
python .\scripts\analyze.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Done. See .\output\pilot_report.md"
