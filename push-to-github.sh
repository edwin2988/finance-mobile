#!/bin/bash
# 推送理财记账手机版到 GitHub
# 运行此脚本后，Git 会记住凭证，以后无需再次输入

cd /home/openclaw/.openclaw/workspace/理财记账手机版

echo "📱 开始推送 陈大哥理财账本 到 GitHub..."
echo "仓库：https://github.com/edwin2988/finance-mobile.git"
echo ""

# 尝试推送（会提示输入用户名和密码）
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "下一步："
    echo "1. 打开 https://github.com/edwin2988/finance-mobile/actions"
    echo "2. 等待 GitHub Actions 自动构建（约 10-20 分钟）"
    echo "3. 下载构建好的 APK 文件"
    echo ""
else
    echo "❌ 推送失败，请检查网络连接和 GitHub 凭证"
    echo ""
    echo "如果提示需要 token，请："
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 创建一个新的 token（勾选 repo 权限）"
    echo "3. 使用 token 作为密码重新推送"
fi
