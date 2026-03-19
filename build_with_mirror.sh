#!/bin/bash

# 使用国内镜像构建APK

echo "=== 使用国内镜像构建APK ==="
echo ""

# 清理之前的构建文件
echo "[1/5] 清理构建文件"
rm -rf bin
rm -rf .buildozer

echo ""

# 设置git镜像
echo "[2/5] 设置git镜像"
git config --global url."https://mirror.ghproxy.com/https://github.com/".insteadOf "https://github.com/"
git config --global url."https://gitee.com/".insteadOf "https://github.com/"

echo ""

# 设置pip镜像
echo "[3/5] 设置pip镜像"
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

echo ""

# 设置Android镜像环境变量
echo "[4/5] 设置Android镜像"
export ANDROID_SDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export ANDROID_NDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export GRADLE_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/gradle/

echo ""

# 开始构建
echo "[5/5] 开始构建APK (这可能需要30-60分钟)..."
echo "使用国内镜像加速构建..."
echo ""

# 执行构建
buildozer android debug

echo ""
echo "=== 构建完成 ==="
