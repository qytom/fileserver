#!/bin/bash

# 设置Android SDK和NDK路径
export ANDROID_HOME=~/Android/Sdk
export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/25.1.8937393
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/33.0.0:$ANDROID_NDK_HOME:$PATH

# 切换到项目目录
cd ~/new_http_server

# 直接使用python-for-android构建APK
echo "开始构建APK..."
python3 -m pythonforandroid.toolchain apk --dist_name=httpserver --bootstrap=sdl2 --requirements=python3,kivy,flask,werkzeug --arch=armeabi-v7a --copy-libs --android-api=31 --ndk-api=21 --package=org.example.httpserver --name=MobileHTTPFileServer --version=1.0 --orientation=portrait --private=/root/new_http_server

# 检查构建结果
echo "构建完成！"
ls -la bin/
