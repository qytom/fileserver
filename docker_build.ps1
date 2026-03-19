$ErrorActionPreference = "Stop"

Write-Host "=== APK Docker Build Script ===" -ForegroundColor Green
Write-Host ""

$ImageName = "m.daocloud.io/docker.io/kivy/python-for-android:latest"
$ProjectPath = $PSScriptRoot

Write-Host "[1/3] Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found"
    }
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker Desktop not installed or not running!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host "Then configure mirror acceleration in Docker Desktop Settings -> Docker Engine:" -ForegroundColor Yellow
    Write-Host '{ "registry-mirrors": ["https://docker.m.daocloud.io"] }' -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "[2/3] Pulling Docker image (first time only)..." -ForegroundColor Yellow
Write-Host "Image: $ImageName" -ForegroundColor Gray
docker pull $ImageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Image pull failed, trying to use cached image..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Building APK..." -ForegroundColor Yellow
Write-Host "Project: $ProjectPath" -ForegroundColor Gray

docker run --rm `
    -v "${ProjectPath}:/app" `
    -w /app `
    $ImageName `
    buildozer android debug

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Build Successful ===" -ForegroundColor Green
    Write-Host "APK location: $ProjectPath\bin\" -ForegroundColor Cyan
    
    $apkFiles = Get-ChildItem -Path "$ProjectPath\bin\*.apk" -ErrorAction SilentlyContinue
    if ($apkFiles) {
        Write-Host ""
        Write-Host "Generated APK files:" -ForegroundColor Green
        foreach ($apk in $apkFiles) {
            $sizeMB = [math]::Round($apk.Length / 1MB, 2)
            Write-Host "  - $($apk.Name) ($sizeMB MB)" -ForegroundColor White
        }
    }
} else {
    Write-Host ""
    Write-Host "=== Build Failed ===" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
