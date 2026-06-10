$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvActivate)) {
    throw "Virtual environment not found at $VenvActivate. Run 'python -m venv venv' first."
}

Write-Host "Starting backend and frontend..."

Start-Process powershell -ArgumentList @(
    "-NoLogo",
    "-NoProfile",
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot'; & '$VenvActivate'; uvicorn backend.main:app --reload"
)

Start-Process powershell -ArgumentList @(
    "-NoLogo",
    "-NoProfile",
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot'; & '$VenvActivate'; python -m streamlit run frontend/streamlit_app.py"
)

Write-Host "Backend and frontend are starting in separate PowerShell windows."
