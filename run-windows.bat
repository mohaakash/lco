@echo off
REM BirthCode Docker Runner for Windows
REM This script sets up and runs the BirthCode application in Docker

echo ========================================
echo BirthCode - Docker Setup for Windows
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/4] Checking for VcXsrv X Server...
tasklist /FI "IMAGENAME eq vcxsrv.exe" 2>NUL | find /I /N "vcxsrv.exe">NUL
if errorlevel 1 (
    echo.
    echo WARNING: VcXsrv X Server is not running!
    echo.
    echo To run this GUI application, you need an X Server for Windows.
    echo.
    echo Please follow these steps:
    echo 1. Download VcXsrv from: https://sourceforge.net/projects/vcxsrv/
    echo 2. Install VcXsrv
    echo 3. Run XLaunch from Start Menu
    echo 4. Use these settings:
    echo    - Multiple windows
    echo    - Display number: 0
    echo    - Start no client
    echo    - Check "Disable access control"
    echo 5. IMPORTANT: Allow VcXsrv through Windows Firewall when prompted
    echo    - Or manually add firewall rule for vcxsrv.exe
    echo 6. Run this script again
    echo.
    pause
    exit /b 1
) else (
    echo VcXsrv is running - OK
)

echo.
echo [2/4] Building Docker image...
docker-compose build
if errorlevel 1 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)

echo.
echo [3/4] Setting up X11 display...
REM Get the host IP for WSL2
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do set HOST_IP=%%a
set HOST_IP=%HOST_IP:~1%
set DISPLAY=%HOST_IP%:0.0

echo Display set to: %DISPLAY%

echo.
echo [4/4] Starting BirthCode application...
echo.
docker-compose run --rm -e DISPLAY=%DISPLAY% birthcode-app

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    echo Troubleshooting tips:
    echo 1. Make sure VcXsrv is running with "Disable access control" checked
    echo 2. Check Windows Firewall settings:
    echo    - Allow VcXsrv (vcxsrv.exe) through firewall
    echo    - Allow Docker Desktop through firewall
    echo 3. Try restarting VcXsrv and Docker Desktop
    echo 4. If using antivirus software, ensure it's not blocking connections
    pause
    exit /b 1
)

echo.
echo Application closed successfully.
pause
