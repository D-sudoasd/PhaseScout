@echo off
setlocal
title PhaseScout
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3.12 -m venv .venv 2>nul
    if errorlevel 1 py -3 -m venv .venv
)

call ".venv\Scripts\activate.bat"

python -c "import mp_api" >nul 2>nul
if errorlevel 1 (
    python -m pip install -r requirements.txt
)

python app.py
if errorlevel 1 pause
