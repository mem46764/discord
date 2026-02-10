@echo off
REM Discord Backup Bot Startup Script for Windows

echo ==========================================
echo   Discord Backup Bot
echo ==========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found
    echo.
    echo Please create a .env file with your Discord bot token:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and add your DISCORD_TOKEN
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Discord Backup Bot...
echo Press Ctrl+C to stop
echo.

REM Run the bot
python bot.py

pause
