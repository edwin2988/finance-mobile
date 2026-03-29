# 📱 陈大哥理财账本 - APK 生成指南

## 🎯 目标
生成安卓 APK 安装包，让手机可以安装使用。

## 📋 准备工作
1. 一个 GitHub 账号（如果没有，去 https://github.com 注册一个）
2. 电脑上安装 Git（https://git-scm.com/）

---

## 🚀 方案 A：使用 GitHub Actions 自动构建（推荐！）

### 第 1 步：创建 GitHub 仓库
1. 打开 https://github.com/new
2. 仓库名：`finance-tracker-mobile`
3. 可见性：**Public**（公开，免费使用 Actions）
4. 点击 "Create repository"

### 第 2 步：上传代码到 GitHub
打开命令行（CMD 或 PowerShell），进入项目目录：
```bash
cd E:\记账手机版
```

初始化 Git 仓库：
```bash
git init
git add .
git commit -m "Initial commit"
```

连接到 GitHub 仓库（替换 `<你的用户名>` 为你的 GitHub 用户名）：
```bash
git remote add origin https://github.com/<你的用户名>/finance-tracker-mobile.git
git branch -M main
git push -u origin main
```

### 第 3 步：启用 GitHub Actions
1. 打开刚创建的 GitHub 仓库页面
2. 点击顶部菜单的 **"Actions"** 标签
3. 如果是第一次使用，点击 **"I understand my workflows, go ahead and enable them"**

### 第 4 步：触发构建
代码上传后会自动触发构建。如果没有自动触发：
1. 点击 **"Actions"** → 左侧选择 **"Build Android APK"**
2. 点击右上角 **"Run workflow"**
3. 选择 **"main"** 分支，点击 **"Run workflow"**

### 第 5 步：下载 APK
等待构建完成（约 10-20 分钟）：
1. 刷新 Actions 页面，看到绿色对勾表示成功
2. 点击最新的构建记录
3. 在页面底部找到 **"Artifacts"**
4. 点击 **"finance-app"** 下载
5. 解压下载的 ZIP 文件，得到 APK

---

## 📲 方案 B：本地构建（高级用户）

### 环境要求
- Linux 系统（或 WSL）
- Python 3.8-3.11
- Android SDK
- OpenJDK 8/11
- Buildozer

### 安装依赖
```bash
sudo apt-get update
sudo apt-get install -y git ffmpeg cmake libgtk-3-dev libgl1-mesa-dev libegl1-mesa-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good python3-pip
pip3 install buildozer
```

### 构建 APK
```bash
cd /path/to/finance_tracker_mobile
buildozer init
buildozer android debug
```

构建完成后，APK 在 `bin/` 目录下。

---

## 📱 安装到手机

### 方法 1：直接安装
1. 将 APK 文件传到手机
2. 在手机上打开 APK 文件
3. 允许安装未知来源应用
4. 点击安装

### 方法 2：通过 ADB 安装
```bash
adb install bin/陈大哥理财账本-1.0.0-debug.apk
```

---

## ⚠️ 常见问题

### Q1: GitHub Actions 构建失败？
**A:** 检查 `buildozer.spec` 中的配置，确保：
- `requirements` 正确
- `android.api` 不超过 31（推荐 31）

### Q2: 构建时间太长？
**A:** 正常现象，第一次构建需要下载大量依赖（10-20 分钟）。

### Q3: APK 无法安装？
**A:** 
- 确保手机允许安装未知来源应用
- 检查 APK 是否完整下载
- 尝试 Android 版本兼容性（最低 Android 5.0）

### Q4: 代码修改后如何重新构建？
**A:**
```bash
git add .
git commit -m "更新内容"
git push
```
GitHub Actions 会自动重新构建！

---

## 📂 项目文件说明
```
理财记账手机版/
├── main_kivy.py              # 主程序代码
├── buildozer.spec            # Buildozer 配置
├── requirements.txt          # Python 依赖
└── .github/workflows/
    └── build.yml             # GitHub Actions 配置
```

---

## 🎉 成功标志
- [x] GitHub Actions 显示绿色对勾
- [x] 下载到 `finance-app.zip` 文件
- [x] 解压得到 `.apk` 文件
- [x] 手机成功安装并打开应用

---

**下一步：** 将 `main_kivy.py`、`buildozer.spec`、`requirements.txt` 上传到 GitHub 仓库，然后触发自动构建！

**开发完成日期：** 2026-03-29
