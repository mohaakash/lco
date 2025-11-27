@echo off
REM Package BirthCode for Client Distribution (Windows)
REM This script creates a clean ZIP file for your client

echo Creating client package for BirthCode...
echo.

REM Check if 7-Zip or PowerShell is available
where 7z >nul 2>&1
if %errorlevel% equ 0 (
    echo Using 7-Zip...
    call :create_with_7zip
    goto :done
)

echo Using PowerShell...
call :create_with_powershell
goto :done

:create_with_7zip
7z a -tzip birthcode-client-package.zip ^
  main.py ^
  requirements.txt ^
  Dockerfile ^
  docker-compose.yml ^
  .dockerignore ^
  run-windows.bat ^
  DOCKER_SETUP.md ^
  README.md ^
  .env.example ^
  ai ^
  calc ^
  ui ^
  fonts ^
  images ^
  -x!*.pyc ^
  -x!__pycache__ ^
  -x!.git ^
  -x!.venv ^
  -x!venv ^
  -x!.env ^
  -x!tests ^
  -x!docs ^
  -x!*.spec ^
  -x!build ^
  -x!dist
goto :eof

:create_with_powershell
powershell -Command "& { ^
  $files = @( ^
    'main.py', ^
    'requirements.txt', ^
    'Dockerfile', ^
    'docker-compose.yml', ^
    '.dockerignore', ^
    'run-windows.bat', ^
    'DOCKER_SETUP.md', ^
    'README.md', ^
    '.env.example', ^
    'ai', ^
    'calc', ^
    'ui', ^
    'fonts', ^
    'images' ^
  ); ^
  Compress-Archive -Path $files -DestinationPath 'birthcode-client-package.zip' -Force ^
}"
goto :eof

:done
echo.
echo ========================================
echo Package created: birthcode-client-package.zip
echo ========================================
echo.
echo Ready to send to your client!
echo.
pause
