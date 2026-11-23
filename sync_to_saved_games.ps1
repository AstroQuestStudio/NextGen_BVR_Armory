param(
    [string]$Target = "$env:USERPROFILE\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory"
)

$Source = Join-Path $PSScriptRoot "mod"
if (-not (Test-Path $Source)) {
    throw "Source folder not found: $Source"
}

Write-Host "Syncing NextGen_BVR_Armory from '$Source' to '$Target'..."
New-Item -ItemType Directory -Force -Path $Target | Out-Null
robocopy $Source $Target /MIR /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "Robocopy failed with exit code $LASTEXITCODE"
}
Write-Host "[OK] Mod synced cleanly to $Target"
