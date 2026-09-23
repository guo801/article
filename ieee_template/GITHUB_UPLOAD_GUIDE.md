# GitHub 上传指南

## 第一步：安装Git

### Windows系统

1. 访问 Git 官网：https://git-scm.com/downloads
2. 下载 Windows 版本的 Git 安装程序
3. 运行安装程序，使用默认设置即可
4. 安装完成后，重新打开命令行或VSCode

### 验证安装

打开命令行（PowerShell或CMD），输入：

```bash
git --version
```

如果显示版本号，说明安装成功。

## 第二步：创建GitHub仓库

1. 访问 https://github.com 并登录您的账号
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `digital-twin-robotic-framework`（或您喜欢的名称）
   - **Description**: `数字孪生驱动的自动化材料合成混合机器人框架`
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Add a README file"（我们已经有了）
4. 点击 "Create repository" 创建仓库

## 第三步：初始化本地Git仓库

在VSCode中打开终端（Ctrl+`），执行以下命令：

```bash
# 进入项目目录
cd "c:\Users\guo\Desktop\论文\ieee_template"

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 查看状态（可选）
git status

# 提交代码
git commit -m "初始提交：数字孪生驱动的自动化材料合成混合机器人框架"

# 添加远程仓库（替换 YOUR_USERNAME 和 YOUR_REPO_NAME）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 第四步：验证上传

1. 刷新您的GitHub仓库页面
2. 您应该能看到所有文件已上传成功
3. README.md 文件会自动显示在仓库首页

## 后续更新

当您修改了论文内容后，可以使用以下命令更新GitHub：

```bash
# 添加修改的文件
git add .

# 提交修改
git commit -m "更新论文内容：描述您的修改"

# 推送到GitHub
git push
```

## 常见问题

### Q1: 推送时要求输入用户名和密码？

GitHub 现在推荐使用 Personal Access Token 代替密码：

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 选择权限：勾选 `repo`
4. 生成并复制 token
5. 在推送时，用户名输入您的GitHub用户名，密码输入这个token

### Q2: 如何忽略某些文件？

编辑 `.gitignore` 文件，添加要忽略的文件模式。例如：

```
# 忽略所有PDF文件
*.pdf

# 忽略临时文件
*.aux
*.log
```

### Q3: 如何查看提交历史？

```bash
git log --oneline
```

### Q4: 如何回滚到之前的版本？

```bash
# 查看提交历史
git log --oneline

# 回滚到指定版本（替换 COMMIT_HASH）
git reset --hard COMMIT_HASH

# 强制推送
git push --force
```

## 推荐的GitHub仓库描述

```
📄 数字孪生驱动的自动化材料合成混合机器人框架 | A Digital Twin-Driven Hybrid Robotic Framework for Automated Materials Synthesis

✨ 特性：
- 宏微观解耦的混合架构
- 高保真数字孪生仿真
- 大规模并行强化学习
- 姿态感知奖励工程
- 分层技能编排系统

🎯 实验结果：
- 整体成功率：93.3%
- 宏观导航成功率：98.0%
- 液体溢出率：0.0%

🛠️ 技术栈：
- NVIDIA Isaac Sim
- PPO强化学习
- UR3机械臂
- Python / LaTeX
```

## 需要帮助？

如果遇到任何问题，请参考：

- [GitHub官方文档](https://docs.github.com)
- [Git官方文档](https://git-scm.com/doc)
- [VSCode Git集成](https://code.visualstudio.com/docs/editor/versioncontrol)

---

**祝您上传顺利！** 🎉
