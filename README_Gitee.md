# 陈大哥的理财账本 - 一键部署版

## 🚀 快速部署到 Streamlit Cloud

### 第 1 步：上传到 Gitee

```bash
# 1. 在 Gitee 创建仓库：https://gitee.com/new
# 2. 在本地执行：
git init
git add .
git commit -m "陈大哥理财账本 - 初始版本"
git remote add origin https://gitee.com/<你的用户名>/finance.git
git push -u origin master
```

### 第 2 步：部署到 Streamlit Cloud

1. 访问：https://share.streamlit.io/
2. 点击 "Connect to Gitee"
3. 选择你的仓库 `finance`
4. 主文件路径：`main_streamlit.py`
5. 点击 "Deploy"

### 第 3 步：获取链接

部署成功后，你会得到一个链接：
```
https://<你的用户名>-finance.streamlit.app
```

### 第 4 步：手机访问

1. 手机浏览器打开上面的链接
2. 菜单 → "添加到主屏幕"
3. 完成！桌面会出现图标，像 APP 一样使用

---

## 📱 生成 APK（可选）

如果需要 APK 安装包：

1. 使用上面得到的链接
2. 访问：https://www.appsgeyer.com/
3. 选择 "Website" 模板
4. 输入你的 Streamlit 链接
5. 创建 APK → 下载

---

## 🎉 完成！

现在你可以：
- 用手机随时访问
- 数据存储在云端（或本地，取决于配置）
- 自动更新（推送代码后自动重新部署）
