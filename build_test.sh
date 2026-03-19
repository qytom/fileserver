#!/bin/bash

echo "开始构建文件服务器APK..."

# 设置构建参数
buildozer android debug --arch=arm64-v8a,armeabi-v7a

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo "构建完成！"
    # 检查输出目录
    if [ -d "bin" ]; then
        echo "APK文件位于 bin/ 目录"
        ls -la bin/
    else
        echo "bin目录不存在，尝试查找APK文件"
        find . -name "*.apk" -type f
    fi
else
    echo "构建失败！"
    exit 1
fi
