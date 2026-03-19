# APK Docker Build Guide

## Step 1: Install Docker Desktop

1. Download Docker Desktop for Windows:
   https://www.docker.com/products/docker-desktop

2. Install and restart computer

3. Verify installation:
   docker --version

## Step 2: Configure Mirror Acceleration

1. Open Docker Desktop
2. Click Settings (gear icon) top-left
3. Select Docker Engine from left menu
4. Add to JSON config:

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io"
  ]
}
```

5. Click Apply & Restart

## Step 3: Build APK with Docker

### Quick Build (Recommended)
```powershell
cd C:\Users\Administrator\Documents\trae_projects\autodo\new_http_server
.\docker_build.ps1
```

### Manual Build
```powershell
# Pull image (first time only, ~2GB)
docker pull m.daocloud.io/docker.io/kivy/python-for-android:latest

# Build APK
docker run --rm -v ${PWD}:/app -w /app m.daocloud.io/docker.io/kivy/python-for-android:latest buildozer android debug
```

## Benefits

- **Fast**: Pre-configured build environment
- **Consistent**: Same results every time
- **Isolated**: No system pollution
- **Cache**: Mirror acceleration for China

## Build Time Comparison

| Method | First Build | Rebuild |
|--------|-------------|---------|
| WSL Buildozer | 30-60 min | 10-15 min |
| Docker | 5-10 min | 3-5 min |

## Troubleshooting

### Docker not found
- Ensure Docker Desktop is running
- Restart PowerShell terminal

### Permission denied
- Run PowerShell as Administrator

### Build fails
- Check internet connection
- Verify mirror configuration
