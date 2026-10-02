$ErrorActionPreference = "Stop"
$t = az account get-access-token --resource-type ms-graph --query accessToken -o tsv
$p = $t.Split('.')[1]
$p += '=' * ((4-$p.Length%4)%4)
$payload = [Text.Encoding]::UTF8.GetString(
  [Convert]::FromBase64String($p.Replace('-','+').Replace('_','/'))
) | ConvertFrom-Json

Write-Host "Current Microsoft Graph delegated scopes:"
Write-Host $payload.scp
Write-Host ""
Write-Host "Feature requirements:"
Write-Host "Planner read/write : Group.ReadWrite.All (or suitable Planner delegated access)"
Write-Host "Microsoft To Do    : Tasks.Read / Tasks.ReadWrite"
Write-Host "Outlook Email      : Mail.Read"
Write-Host "Calendar           : Calendars.Read"
Write-Host ""
Write-Host "If a scope is missing, consent must be granted by your Microsoft tenant policy."
