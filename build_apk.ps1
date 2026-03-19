#!/usr/bin/env pwsh
# 简化版APK构建脚本

Write-Host "=== APK构建开始 ==="
Write-Host ""

# 清理之前的构建文件
Write-Host "[1/4] 清理构建文件"
Remove-Item -Path "bin" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".buildozer" -Recurse -Force -ErrorAction SilentlyContinue

# 构建APK
Write-Host "[2/4] 开始构建APK (这可能需要30-60分钟)..."
Write-Host "正在执行: buildozer android debug"
Write-Host ""

# 直接执行buildozer命令
try {
    # 使用--yes参数自动回答确认
    $env:BUILDozER_ALLOW_ROOT = "1"
    & buildozer android debug --yes
} catch {
    Write-Host "构建过程中出错: $_"
    exit 1
}

# 检查构建结果
Write-Host ""
Write-Host "[3/4] 检查构建结果"
$apkPath = "bin\fileserver-1.0-armeabi-v7a-debug.apk"
if (Test-Path -Path $apkPath) {
    Write-Host "✅ 构建成功！"
    Write-Host "APK文件: $apkPath"
    Get-ChildItem -Path "bin\*.apk" | Format-Table -Property Name, Length
    
    # 复制到主目录
    $destPath = "fileserver-3.0-final.apk"
    Copy-Item -Path $apkPath -Destination $destPath -Force
    Write-Host "APK已复制到: $destPath"
} else {
    Write-Host "❌ 构建失败！"
    Write-Host "请检查错误信息"
    exit 1
}

Write-Host ""
Write-Host "=== 构建完成 ==="
