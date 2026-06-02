$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    & $VenvPython -m streamlit run frontend/streamlit_app.py
}
else {
    python -m streamlit run frontend/streamlit_app.py
}
