$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    & $VenvPython -m uvicorn backend.main:app --reload
}
else {
    python -m uvicorn backend.main:app --reload
}
