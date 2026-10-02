param(
  [string]$PlanUrl = "",
  [string]$PlanId = ""
)

$ErrorActionPreference = "Stop"

function Get-PlanIdFromUrl([string]$url) {
  if ($url -match "/plan/([^/]+)/") { return $Matches[1] }
  return ""
}

Write-Host "Todo Agent - Microsoft Planner Connector"

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
  throw "Azure CLI not found"
}

$acct = az account show --output json 2>$null | ConvertFrom-Json
if (-not $acct) {
  throw "Azure CLI is not logged in. Run: az login"
}

Write-Host ("Signed in: " + $acct.user.name)

if (-not $PlanId -and $PlanUrl) {
  $PlanId = Get-PlanIdFromUrl $PlanUrl
}

if (-not $PlanId) {
  Write-Host "Available Planner plans:"
  az rest --method get --url "https://graph.microsoft.com/v1.0/me/planner/plans" --output json
  exit 0
}

$plan = az rest --method get --url "https://graph.microsoft.com/v1.0/planner/plans/$PlanId" --output json | ConvertFrom-Json
Write-Host ("Connected plan: " + $plan.title)
Write-Host ("Plan ID: " + $plan.id)

$bucket = az rest --method get --url "https://graph.microsoft.com/v1.0/planner/plans/$PlanId/buckets" --output json | ConvertFrom-Json
$tasks = az rest --method get --url "https://graph.microsoft.com/v1.0/planner/plans/$PlanId/tasks" --output json | ConvertFrom-Json

Write-Host ("Buckets: " + $bucket.value.Count)
Write-Host ("Tasks: " + $tasks.value.Count)
