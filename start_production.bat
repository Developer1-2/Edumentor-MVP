@echo off
REM Start Edumentor MVP (production-like) using uvicorn
REM Run this from project root: start_production.bat

REM Ensure Python environment is active (activate your venv first if needed)
REM Example (PowerShell): .\venv\Scripts\Activate.ps1

set HOST=0.0.0.0
set PORT=8000
set WORKERS=4

echo Starting Edumentor API on %HOST%:%PORT% with %WORKERS% workers...
python -m uvicorn routes.main:app --host %HOST% --port %PORT% --workers %WORKERS%
pause
