#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包文件服务器为EXE文件
"""

import os
import subprocess
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

def build_exe():
    """使用PyInstaller打包EXE文件"""
    print("开始打包EXE文件...")
    print(f"当前目录: {current_dir}")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 构建命令
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--name", "FileServer",
        "--windowed",
        "main.py"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    # 执行构建
    try:
        result = subprocess.run(
            cmd,
            cwd=current_dir,
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print("\n✅ EXE文件打包成功！")
            print(f"可执行文件位置: {os.path.join(current_dir, 'dist', 'FileServer.exe')}")
        else:
            print(f"\n❌ 打包失败，返回码: {result.returncode}")
    except Exception as e:
        print(f"\n❌ 打包过程中出错: {e}")

if __name__ == "__main__":
    build_exe()
