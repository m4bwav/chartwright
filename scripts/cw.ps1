# Windows launcher: .\scripts\cw.ps1 <command> [args]
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }
& $py.Source (Join-Path $PSScriptRoot "cw.py") @args
exit $LASTEXITCODE
