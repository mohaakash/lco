@echo off
echo -------------------------------------------
echo  Starting Qt GUI App inside Docker
echo -------------------------------------------

REM ---- STEP 1: Start VcXsrv if not running ----
echo Checking VcXsrv...

tasklist /FI "IMAGENAME eq vcxsrv.exe" | find /I "vcxsrv.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo VcXsrv not running. Launching it now...
    start "" "C:\Program Files\VcXsrv\vcxsrv.exe" :0 -multiwindow -clipboard -primary -ac
    timeout /t 2 >nul
) else (
    echo VcXsrv is already running.
)

REM ---- STEP 2: Set DISPLAY environment variable ----
echo Setting DISPLAY variable...
set DISPLAY=host.docker.internal:0.0

REM ---- STEP 3: Run Docker container ----
echo Running Docker container...
docker run ^
  -e DISPLAY=host.docker.internal:0.0 ^
  -v /tmp/.X11-unix:/tmp/.X11-unix ^
  -v "C:\Users":"/app/c_drive/" ^
  akash/v1:latest

echo -------------------------------------------
echo  Qt App closed. Press any key to exit.
echo -------------------------------------------
pause
