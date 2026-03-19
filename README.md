# FileServer - 文件服务器应用

一个基于Kivy框架的跨平台文件服务器应用，支持Android和Windows平台。

## 功能特点

- 📁 文件浏览和下载
- 🌐 HTTP服务器
- 📱 Android权限管理
- 🚀 断点续传支持
- 💾 大文件传输优化

## 使用GitHub Actions构建APK

### 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 创建新仓库（例如：fileserver）
3. 不要初始化README、.gitignore或license

### 步骤2：推送代码到GitHub

```bash
# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/fileserver.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 步骤3：触发自动构建

推送代码后，GitHub Actions会自动开始构建APK。

### 步骤4：下载APK

1. 访问仓库的Actions页面
2. 点击最新的workflow运行
3. 在Artifacts部分下载`fileserver-apk`
4. 或者在Releases页面下载最新版本

## 本地构建

### Windows EXE

```bash
python build_exe.py
```

### Android APK

```bash
buildozer android debug
```

## 权限说明

Android应用需要以下权限：
- INTERNET - 网络访问
- READ_EXTERNAL_STORAGE - 读取存储
- WRITE_EXTERNAL_STORAGE - 写入存储
- ACCESS_NETWORK_STATE - 网络状态
- ACCESS_WIFI_STATE - WiFi状态

## 使用方法

1. 安装APK到手机
2. 授予存储权限
3. 选择要共享的目录
4. 点击"启动服务"
5. 使用其他设备访问显示的IP地址和端口

## 技术栈

- Python 3.8+
- Kivy - 跨平台UI框架
- Buildozer - Android打包工具
- PyInstaller - Windows打包工具

## 许可证

MIT License
