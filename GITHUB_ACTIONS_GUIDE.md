# 使用GitHub Actions构建APK指南

## 准备工作

1. 确保您有GitHub账号
2. 如果没有，请访问 https://github.com/signup 注册

## 步骤1：创建GitHub仓库

1. 登录GitHub
2. 点击右上角的"+"号，选择"New repository"
3. 填写仓库信息：
   - Repository name: fileserver
   - Description: 文件服务器应用
   - 选择"Public"或"Private"
   - **不要勾选** "Add a README file"
   - **不要勾选** "Add .gitignore"
   - **不要勾选** "Choose a license"
4. 点击"Create repository"

## 步骤2：安装Git（如果还没有）

### Windows:
1. 访问 https://git-scm.com/download/win
2. 下载并安装Git
3. 安装完成后重启PowerShell

### 或者使用WSL:
```bash
sudo apt-get update
sudo apt-get install git
```

## 步骤3：配置Git

```bash
# 配置用户名和邮箱
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱"

# 配置GitHub认证（选择一种方式）

# 方式1：使用Personal Access Token（推荐）
# 1. 访问 https://github.com/settings/tokens
# 2. 点击"Generate new token (classic)"
# 3. 勾选"repo"权限
# 4. 生成token并保存

# 方式2：使用SSH密钥
# 1. 生成SSH密钥
ssh-keygen -t ed25519 -C "您的邮箱"
# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub
# 3. 添加到GitHub: Settings -> SSH and GPG keys -> New SSH key
```

## 步骤4：初始化本地仓库

```bash
# 进入项目目录
cd /mnt/c/Users/Administrator/Documents/trae_projects/autodo/new_http_server

# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: FileServer application with permission fixes"
```

## 步骤5：推送到GitHub

```bash
# 添加远程仓库（使用HTTPS）
git remote add origin https://github.com/您的用户名/fileserver.git

# 或者使用SSH
git remote add origin git@github.com:您的用户名/fileserver.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 步骤6：查看构建进度

1. 访问您的GitHub仓库
2. 点击"Actions"标签
3. 查看最新的workflow运行
4. 构建通常需要15-30分钟

## 步骤7：下载APK

### 方式1：从Artifacts下载
1. 在Actions页面，点击完成的workflow
2. 滚动到底部"Artifacts"部分
3. 点击"fileserver-apk"下载

### 方式2：从Releases下载
1. 点击仓库右侧的"Releases"
2. 下载最新版本的APK

## 故障排除

### 问题1：推送时需要认证
**解决方案**：使用Personal Access Token作为密码

### 问题2：构建失败
**解决方案**：
1. 查看Actions日志
2. 检查错误信息
3. 修复问题后重新推送

### 问题3：权限问题
**解决方案**：
1. 确保仓库是Public，或者
2. 在Settings -> Actions -> General中启用"Read and write permissions"

## 快速命令（复制粘贴）

```bash
# 完整流程
cd /mnt/c/Users/Administrator/Documents/trae_projects/autodo/new_http_server
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/您的用户名/fileserver.git
git branch -M main
git push -u origin main
```

## 下一步

推送成功后，GitHub Actions会自动开始构建。您可以：
1. 查看构建日志
2. 等待构建完成
3. 下载APK文件
4. 安装到手机测试

## 注意事项

- 首次构建可能需要20-30分钟
- 构建过程会下载大量依赖
- 确保网络连接稳定
- 如果构建失败，可以重新运行workflow
