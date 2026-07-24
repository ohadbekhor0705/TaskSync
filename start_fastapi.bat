@echo off
cd /d "C:\Users\User\Documents\GitHub\TaskSync\Backend\app"
call ".venv\Scripts\activate.bat"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
