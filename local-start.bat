@echo off
setlocal

:: Default port
set APP_PORT=5000

:: If an argument was given, use it as the port
if not "%~1"=="" (
    set APP_PORT=%1
)

echo Starting the application on port %APP_PORT%...

:: Check if Docker is installed
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop and try again.
    exit /b 1
)

:: Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    exit /b 1
)

:: Check if port 5432 is in use
netstat -ano | findstr ":5432" >nul
if %ERRORLEVEL%==0 (
    echo [ERROR] Port 5432 is already in use. Please stop the process using it or change the port in docker-compose.yml.
    exit /b 1
)

:: Set environment variable and start docker compose
set APP_PORT=%APP_PORT%
docker compose up --build

if errorlevel 1 (
    echo.
    echo [ERROR] Docker Compose failed to start. Maybe port %APP_PORT% was already in use?
    echo.
    echo Usage: local-start.bat [PORT]
    echo Example: local-start.bat 5001
    exit /b 1
)

endlocal