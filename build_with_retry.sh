#!/bin/bash

# 使用国内镜像构建APK，带有重试机制

echo "=== 使用国内镜像构建APK (带重试机制) ==="
echo ""

# 清理之前的构建文件
echo "[1/6] 清理构建文件"
rm -rf bin
rm -rf .buildozer

echo ""

# 设置git镜像
echo "[2/6] 设置git镜像"
git config --global url."https://mirror.ghproxy.com/https://github.com/".insteadOf "https://github.com/"
git config --global url."https://gitee.com/".insteadOf "https://github.com/"

echo ""

# 设置pip镜像
echo "[3/6] 设置pip镜像"
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

echo ""

# 设置Android镜像环境变量
echo "[4/6] 设置Android镜像"
export ANDROID_SDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export ANDROID_NDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export GRADLE_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/gradle/

echo ""

# 开始构建，带重试机制
echo "[5/6] 开始构建APK (这可能需要30-60分钟)..."
echo "使用国内镜像加速构建..."
echo "构建过程中如果遇到网络问题会自动重试..."
echo ""

# 最大重试次数
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "构建尝试 $((RETRY_COUNT + 1))/$MAX_RETRIES"
    echo ""
    
    # 执行构建
    buildozer android debug
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 构建成功！"
        break
    else
        echo ""
        echo "❌ 构建失败，正在重试..."
        echo ""
        RETRY_COUNT=$((RETRY_COUNT + 1))
        
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "等待30秒后重试..."
            sleep 30
        else
            echo "❌ 构建失败，已达到最大重试次数"
            exit 1
        fi
    fi
done

echo ""

# 检查构建结果
echo "[6/6] 检查构建结果"
if [ -d "bin" ] && [ "$(ls -A bin)" ]; then
    echo "✅ 构建成功！"
    echo "APK文件:"
    ls -la bin/
    
    # 复制到主目录
    cp bin/*.apk fileserver-latest.apk 2>/dev/null || true
    if [ -f "fileserver-latest.apk" ]; then
        echo "APK已复制到: fileserver-latest.apk"
    fi
else
    echo "❌ 构建失败！"
    echo "请检查错误信息"
    exit 1
fi

echo ""
echo "=== 构建完成 ==="
