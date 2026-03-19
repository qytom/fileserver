@echo off
chcp 65001 >nul
echo ========================================
echo    APK Docker Build Script
echo ========================================
echo.

docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker not found!
    echo.
    echo Please install Docker Desktop:
    echo https://www.docker.com/products/docker-desktop
    echo.
    echo Then configure mirror in Docker Desktop Settings:
    echo { "registry-mirrors": ["https://docker.m.daocloud.io"] }
    echo.
    pause
    exit /b 1
)

echo [1/3] Docker found
echo.

echo [2/3] Pulling image...
docker pull m.daocloud.io/docker.io/kivy/python-for-android:latest
echo.

echo [3/3] Building APK...
docker run --rm -v "%~dp0:/app" -w /app m.daocloud.io/docker.io/kivy/python-for-android:latest buildozer android debug
echo.

if errorlevel 1 (
    echo [FAILED] Build failed
) else (
    echo [SUCCESS] APK built successfully
    echo Location: %~dp0bin\
    dir /b "%~dp0bin\*.apk" 2>nul
)

echo.
pause
