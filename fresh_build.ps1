#!/usr/bin/env pwsh
# 全新构建脚本 - 完全清理所有缓存

Write-Host "=== 全新APK构建开始 ==="
Write-Host ""

# 1. 创建全新构建目录
$BUILD_DIR = "fresh_build_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "[1/5] 创建全新构建目录: $BUILD_DIR"
New-Item -ItemType Directory -Path $BUILD_DIR -Force
Set-Location -Path $BUILD_DIR

# 2. 复制最新代码
Write-Host "[2/5] 复制最新代码"
Copy-Item -Path "..\main.py" -Destination "." -Force
Copy-Item -Path "..\buildozer.spec" -Destination "." -Force

# 验证代码
Write-Host "验证代码包含版本信息:"
grep "APP_VERSION" main.py | Select-Object -First 1
grep "version_label" main.py | Select-Object -First 1

# 3. 完全清理buildozer缓存
Write-Host ""
Write-Host "[3/5] 完全清理buildozer缓存"
$buildozerCache = Join-Path -Path $env:USERPROFILE -ChildPath ".buildozer"
$p4aCache = Join-Path -Path $env:USERPROFILE -ChildPath ".local\share\python-for-android"

if (Test-Path -Path $buildozerCache) {
    Remove-Item -Path $buildozerCache -Recurse -Force -ErrorAction SilentlyContinue
}

if (Test-Path -Path $p4aCache) {
    Remove-Item -Path $p4aCache -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. 初始化并构建
Write-Host ""
Write-Host "[4/5] 初始化buildozer"
try {
    buildozer init 2>$null
} catch {
    # 忽略错误
}

Write-Host ""
Write-Host "[5/5] 开始构建APK (这可能需要30-60分钟)..."
try {
    buildozer android debug 2>&1 | Tee-Object -FilePath build.log
} catch {
    Write-Host "构建过程中出错: $_"
}

# 5. 复制结果
Write-Host ""
Write-Host "=== 构建完成 ==="
$apkPath = Join-Path -Path "bin" -ChildPath "fileserver-1.0-armeabi-v7a-debug.apk"
if (Test-Path -Path $apkPath) {
    $destPath = Join-Path -Path ".." -ChildPath "fileserver-3.0-fresh.apk"
    Copy-Item -Path $apkPath -Destination $destPath -Force
    Write-Host "APK已复制到: fileserver-3.0-fresh.apk"
    Get-ChildItem -Path "bin\*.apk" | Format-Table -Property Name, Length
} else {
    Write-Host "构建失败，检查 build.log"
    exit 1
}

# 返回原始目录
Set-Location -Path ".."
