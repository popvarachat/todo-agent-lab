$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Todo Agent Lab Bootstrap ==="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python 3.10+ is required."
}
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
  throw "Azure CLI is required for Microsoft providers."
}

if (-not (Test-Path ".\config\settings.json")) {
  Copy-Item ".\config\settings.example.json" ".\config\settings.json"
}

$acct = az account show --output json 2>$null | ConvertFrom-Json
if (-not $acct) {
  Write-Host "Microsoft sign-in required..."
  az login | Out-Null
  $acct = az account show --output json | ConvertFrom-Json
}
Write-Host ("Signed in as: " + $acct.user.name)

Write-Host ""
Write-Host "1 = Microsoft Planner"
Write-Host "2 = Microsoft To Do"
Write-Host "3 = Local JSON demo"
$choice = Read-Host "Choose provider"
$cfg = Get-Content ".\config\settings.json" -Raw | ConvertFrom-Json

if ($choice -eq "1") {
  $url = Read-Host "Paste Planner URL"
  if ($url -notmatch "/plan/([^/]+)/") {
    throw "Could not find Planner Plan ID in the URL."
  }
  $planId = $Matches[1]
  $plan = az rest --method get --url "https://graph.microsoft.com/v1.0/planner/plans/$planId" --output json | ConvertFrom-Json
  $cfg.provider = "microsoft_planner"
  $cfg.plan_id = $planId
  $cfg.plan_name = $plan.title
  Write-Host ("Connected: " + $plan.title)
}
elseif ($choice -eq "2") {
  try {
    $lists = az rest --method get --url "https://graph.microsoft.com/v1.0/me/todo/lists" --output json | ConvertFrom-Json
    $cfg.provider = "microsoft_todo"
    if (-not ($cfg.PSObject.Properties.Name -contains "list_id")) {
      $cfg | Add-Member -NotePropertyName list_id -NotePropertyValue "all"
    } else { $cfg.list_id = "all" }
    Write-Host ("Connected Microsoft To Do. Lists: " + $lists.value.Count)
  }
  catch {
    Write-Host "Microsoft To Do requires delegated Microsoft Graph Tasks.Read permission."
    Write-Host "Planner remains fully usable without this extra permission."
    exit 2
  }
}
else {
  $cfg.provider = "json_file"
  if (-not ($cfg.PSObject.Properties.Name -contains "data_path")) {
    $cfg | Add-Member -NotePropertyName data_path -NotePropertyValue ".\examples\sample_tasks.json"
  } else { $cfg.data_path = ".\examples\sample_tasks.json" }
}
$cfg | ConvertTo-Json -Depth 10 | Set-Content ".\config\settings.json" -Encoding UTF8

Write-Host ""
Write-Host "Running agents..."
python -m todo_agent.cli --config ".\config\settings.json"

Write-Host ""
Write-Host "Done."
Write-Host "Report: .\output\agent_report.md"
Write-Host "JSON:   .\output\agent_result.json"
