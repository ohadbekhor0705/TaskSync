@echo off
TITLE TaskSync Backend API
echo ===================================================
echo [TaskSync] Starting FastAPI Development Server...
echo ===================================================



::  Activate the virtual environment
echo [TaskSync] Activating virtual environment...
call .venv\Scripts\activate

cd Backend/app

::  Run the Uvicorn server
echo [TaskSync] Starting Uvicorn on http://127.0.0.1:8000
echo ---------------------------------------------------
uvicorn main:app --reload

pause