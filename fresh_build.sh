#!/bin/bash
# 全新构建脚本 - 完全清理所有缓存

set -e

echo "=== 全新APK构建开始 ==="
echo ""

# 1. 创建全新构建目录
BUILD_DIR="/root/fresh_build_$(date +%s)"
echo "[1/5] 创建全新构建目录: $BUILD_DIR"
mkdir -p $BUILD_DIR
cd $BUILD_DIR

# 2. 复制最新代码
echo "[2/5] 复制最新代码"
cp /mnt/c/Users/Administrator/Documents/trae_projects/autodo/new_http_server/main.py .
cp /mnt/c/Users/Administrator/Documents/trae_projects/autodo/new_http_server/buildozer.spec .

# 验证代码
echo "验证代码包含版本信息:"
grep "APP_VERSION" main.py | head -1
grep "version_label" main.py | head -1

# 3. 完全清理buildozer缓存
echo ""
echo "[3/5] 完全清理buildozer缓存"
rm -rf ~/.buildozer
rm -rf /root/new_http_server/.buildozer
rm -rf /root/.local/share/python-for-android

# 4. 初始化并构建
echo ""
echo "[4/5] 初始化buildozer"
buildozer init 2>/dev/null || true

echo ""
echo "[5/5] 开始构建APK (这可能需要30-60分钟)..."
buildozer android debug 2>&1 | tee build.log

# 5. 复制结果
echo ""
echo "=== 构建完成 ==="
if [ -f "bin/fileserver-1.0-armeabi-v7a_arm64-v8a-debug.apk" ]; then
    cp bin/fileserver-1.0-armeabi-v7a_arm64-v8a-debug.apk /mnt/c/Users/Administrator/Documents/trae_projects/autodo/new_http_server/fileserver-3.0-fresh.apk
    echo "APK已复制到: fileserver-3.0-fresh.apk"
    ls -lh bin/*.apk
else
    echo "构建失败，检查 build.log"
    exit 1
fi
