$ErrorActionPreference = "Stop"

Write-Host "=== Docker Mirror Configuration Helper ===" -ForegroundColor Green
Write-Host ""

Write-Host "This script will help you configure Docker mirror acceleration for faster image pulls in China."
Write-Host ""

Write-Host "Step 1: Open Docker Desktop" -ForegroundColor Yellow
Write-Host "  - Make sure Docker Desktop is running"
Write-Host ""

Write-Host "Step 2: Configure Mirror" -ForegroundColor Yellow
Write-Host "  1. Click the gear icon (Settings) in Docker Desktop"
Write-Host "  2. Select 'Docker Engine' from the left menu"
Write-Host "  3. Add the following to the JSON configuration:"
Write-Host ""

$config = @"
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io"
  ]
}
"@

Write-Host $config -ForegroundColor Cyan
Write-Host ""

Write-Host "  4. Click 'Apply & Restart'"
Write-Host ""

Write-Host "Step 3: Verify Configuration" -ForegroundColor Yellow
Write-Host "  Run: docker info" -ForegroundColor Gray
Write-Host "  Look for 'Registry Mirrors' in the output"
Write-Host ""

Write-Host "=== Quick Test ===" -ForegroundColor Green
Write-Host "Testing Docker connection..."

try {
    $info = docker info 2>&1 | Out-String
    if ($info -match "Registry Mirrors") {
        Write-Host "Mirror configuration detected!" -ForegroundColor Green
        Write-Host $info -ForegroundColor Gray
    } else {
        Write-Host "No mirror configured yet. Please follow the steps above." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Docker not running or not installed." -ForegroundColor Red
}

Write-Host ""
Write-Host "After configuration, run: .\docker_build.ps1" -ForegroundColor Green
Write-Host ""
