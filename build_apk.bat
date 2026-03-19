@echo off

setlocal

echo === APK构建开始 ===
echo.

:: 清理之前的构建文件
echo [1/4] 清理构建文件
if exist bin rmdir /s /q bin
if exist .buildozer rmdir /s /q .buildozer

echo.

:: 构建APK
echo [2/4] 开始构建APK (这可能需要30-60分钟)...
echo 正在执行: buildozer android debug
echo.

:: 设置环境变量
gset BUILDOZER_ALLOW_ROOT=1

:: 执行构建
buildozer android debug

echo.

:: 检查构建结果
echo [3/4] 检查构建结果
if exist bin\*.apk (
    echo ✅ 构建成功！
    echo APK文件:
    dir bin\*.apk
    
    :: 复制到主目录
    set "APK_FILE="
    for /f "delims=" %%f in ('dir /b /o:-d bin\*.apk') do (
        if not defined APK_FILE set "APK_FILE=%%f"
    )
    
    if defined APK_FILE (
        copy "bin\%APK_FILE%" "fileserver-3.0-permission.apk" /y
        echo APK已复制到: fileserver-3.0-permission.apk
    )
) else (
    echo ❌ 构建失败！
    echo 请检查错误信息
    exit /b 1
)

echo.
echo === 构建完成 ===

endlocal
pause
