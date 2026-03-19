# APK构建指南

本指南记录了完整的APK构建步骤，使用国内镜像加速构建过程。

## 构建环境准备

### 1. 系统要求
- Windows 10/11
- WSL (Windows Subsystem for Linux) 已安装
- Ubuntu 分发版
- Python 3.7+
- Buildozer

### 2. 安装依赖

在WSL中执行以下命令：

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装必要依赖
sudo apt install -y git python3-pip python3-dev build-essential openjdk-17-jdk unzip zip

# 安装buildozer
pip3 install --upgrade pip
pip3 install buildozer

# 初始化buildozer（第一次运行时）
buildozer init
```

## 构建步骤

### 步骤1: 清理构建环境

```bash
# 清理之前的构建文件
rm -rf bin
rm -rf .buildozer
```

### 步骤2: 配置国内镜像

```bash
# 设置git镜像
git config --global url."https://mirror.ghproxy.com/https://github.com/".insteadOf "https://github.com/"

# 设置pip镜像
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

# 设置Android镜像环境变量
export ANDROID_SDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export ANDROID_NDK_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/android/repository/
export GRADLE_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/gradle/
```

### 步骤3: 配置buildozer.spec

确保`buildozer.spec`文件包含以下配置：

```ini
# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_WIFI_STATE

# (str) Android SDK mirror
android.sdk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Android NDK mirror
android.ndk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Gradle mirror
android.gradle_mirror = https://mirrors.tuna.tsinghua.edu.cn/gradle/

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version
tools.android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (str) Android arch
tools.android.arch = armeabi-v7a
```

### 步骤4: 执行构建

```bash
# 执行构建命令
buildozer android debug
```

### 步骤5: 检查构建结果

构建完成后，APK文件会生成在`bin`目录中：

```bash
# 查看构建结果
ls -la bin/

# 复制到主目录
cp bin/*.apk fileserver-latest.apk
```

## 一键构建脚本

### 使用国内镜像的构建脚本

```bash
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

# 检查构建结果
echo "[6/6] 检查构建结果"
if [ -f "bin/*.apk" ]; then
    echo "✅ 构建成功！"
    echo "APK文件:"
    ls -la bin/
    
    # 复制到主目录
    cp bin/*.apk fileserver-latest.apk
    echo "APK已复制到: fileserver-latest.apk"
else
    echo "❌ 构建失败！"
    echo "请检查错误信息"
    exit 1
fi

echo ""
echo "=== 构建完成 ==="
```

### 在WSL中运行构建脚本

```bash
# 赋予脚本执行权限
chmod +x build_with_mirror.sh

# 运行构建脚本
./build_with_mirror.sh
```

## 常见问题解决

### 1. 构建速度慢
- 确保使用了国内镜像
- 检查网络连接
- 第一次构建会下载大量依赖，后续构建会快很多

### 2. 权限错误
- 确保`buildozer.spec`中配置了正确的权限
- 确保应用代码中实现了权限检查

### 3. 内存不足
- 增加WSL的内存分配
- 修改`buildozer.spec`中的`android.gradle_memory`参数

### 4. SDK/NDK下载失败
- 检查网络连接
- 确认镜像地址正确
- 手动下载SDK/NDK并放置到相应目录

## 构建时间预估

- **第一次构建**：30-60分钟（需要下载SDK、NDK和依赖项）
- **后续构建**：10-20分钟（缓存已建立）

## 输出文件

- **APK文件**：`bin/fileserver-1.0-armeabi-v7a-debug.apk`
- **构建日志**：`.buildozer/android/build.log`
- **打包后的EXE**：`dist/FileServer.exe`

## 版本历史

- **v3.0**：修复权限问题，使用国内镜像加速构建
- **v2.5**：优化文件传输速度，支持断点续传
- **v2.0**：中文化界面，修复乱码问题
- **v1.0**：初始版本

---

**注意**：构建过程中请保持网络连接稳定，第一次构建可能需要较长时间，请耐心等待。
