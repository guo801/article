# 数字孪生驱动的自动化材料合成混合机器人框架

A Digital Twin-Driven Hybrid Robotic Framework for Automated Materials Synthesis

[![LaTeX](https://img.shields.io/badge/LaTeX-IEEE-blue.svg)](https://www.ieee.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📄 论文概述

本文提出了一种数字孪生驱动的混合机器人框架，专为复杂生化实验室工作流的端到端自动化量身定制。

### 主要贡献

1. **宏微观解耦的混合架构**：将宏观液体容器转移委托给约束感知的经典规划器，同时利用深度强化学习实现鲁棒的机械臂操作。

2. **高保真数字孪生中的大规模并行强化学习**：在Isaac Sim中构建物理驱动、张量加速的虚拟沙盒，实现灵巧策略的并行训练。

3. **通过姿态感知奖励实现的鲁棒虚实迁移**：设计密集的奖励工程机制，确保机械臂能够可靠地迁移到真实物理设置中。

4. **用于生物分析的分层技能编排**：构建由元控制器管理的可复用技能基元库，消除灾难性遗忘，保证强大的错误恢复能力。

### 实验结果

- 整体物理执行成功率：**93.3%**
- 宏观导航成功率：**98.0%**
- 姿态感知抓取成功率：**96.0%**
- 液体溢出率：**0.0%**

## 📁 项目结构

```
ieee_template/
├── main.tex                      # 英文版主文档
├── main_chinese.tex              # 中文版主文档
├── sections/                     # 论文章节
│   ├── abstract.tex              # 英文摘要
│   ├── introduction.tex          # 英文引言
│   ├── related_work.tex          # 英文相关工作
│   ├── methodology.tex           # 英文方法论
│   ├── experiments.tex           # 英文实验
│   ├── conclusion.tex            # 英文结论
│   ├── abstract_chinese.tex      # 中文摘要
│   ├── introduction_chinese.tex  # 中文引言
│   ├── related_work_chinese.tex  # 中文相关工作
│   ├── methodology_chinese.tex   # 中文方法论
│   ├── experiments_chinese.tex   # 中文实验
│   └── conclusion_chinese.tex    # 中文结论
├── images/                       # 图片文件夹
│   ├── Framework.png             # 框架图
│   ├── environment_design.png    # 环境设计图
│   ├── Large scale parallel training.png  # 大规模并行训练图
│   ├── skill_lab.png             # 技能库图
│   └── sim and real.png          # 仿真与实物对比图
├── references.bib                # 参考文献库
├── .gitignore                    # Git忽略文件
└── README.md                     # 本说明文件
```

## 🚀 快速开始

### 环境要求

- **LaTeX发行版**：TeX Live 或 MiKTeX
- **编译器**：XeLaTeX（支持中文）
- **操作系统**：Windows / macOS / Linux

### 编译方法

#### 方法一：命令行编译

```bash
# 英文版
xelatex main.tex
xelatex main.tex  # 第二次编译解决交叉引用

# 中文版
xelatex main_chinese.tex
xelatex main_chinese.tex
```

#### 方法二：使用Overleaf

1. 将所有文件打包上传到 [Overleaf](https://www.overleaf.com)
2. 在设置中选择 **XeLaTeX** 编译器
3. 点击编译按钮

#### 方法三：使用VSCode + LaTeX Workshop

1. 安装 [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) 扩展
2. 打开 `main.tex` 或 `main_chinese.tex`
3. 使用快捷键 `Ctrl+Alt+B` 编译

## 🔧 技术栈

- **仿真环境**：NVIDIA Isaac Sim
- **强化学习算法**：PPO (Proximal Policy Optimization)
- **机器人平台**：UR3机械臂 + Robotiq 2F-85夹爪
- **感知系统**：Intel RealSense D435 RGB-D相机
- **计算平台**：NVIDIA RTX 4090

## 📚 参考文献

1. Burger, B. et al. "A mobile robotic chemist." *Nature* (2020)
2. MacLeod, B. P. et al. "Self-driving laboratory for accelerated discovery of thin-film materials." *Science Advances* (2020)
3. Makoviychuk, V. et al. "Isaac Gym: High performance GPU-based physics simulation for robot learning." *NeurIPS* (2021)

## 📧 联系方式

如有任何问题，请通过以下方式联系：

- **作者**：cx guo
- **邮箱**：[请添加您的邮箱]

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢 NVIDIA 提供的 Isaac Sim 仿真平台，以及所有参考文献的作者们。

---

**最后更新**：2026年5月
