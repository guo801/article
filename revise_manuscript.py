from pathlib import Path
import re, shutil, math, datetime

root = Path(r'C:\Users\guo\Desktop\article\ieee_template')
backup = root / ('revision_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
backup.mkdir()
for name in ['main.tex','main_chinese.tex','main_standalone.tex','README.md','main.pdf','main_chinese.pdf','main_standalone.pdf']:
    if (root/name).exists(): shutil.copy2(root/name, backup/name)
shutil.copytree(root/'sections', backup/'sections')
old = {p.stem:p.read_text(encoding='utf-8') for p in (root/'sections').glob('*.tex')}

def write(name, text):
    (root/name).write_text(text.strip()+'\n', encoding='utf-8')

def section(name,en,zh):
    write('sections/'+name+'.tex',en)
    write('sections/'+name+'_chinese.tex',zh)

section('abstract',r'''
\begin{abstract}
Laboratory liquid handling combines container transport, contact-rich grasping, and demonstration-dependent manipulation. These operations have different control requirements and are difficult to accommodate with a single policy. We present a digital twin-assisted hybrid robotic framework that combines constrained motion planning for transport, posture-aware reinforcement learning for grasping, and imitation learning with real-world fine-tuning for pipetting and dispensing. An Isaac Sim environment supports policy training, while a hierarchical state machine coordinates the execution of reusable skills. The evaluation focuses on navigation, upright grasping, reagent pipetting, droplet dispensing, and serial dilution-related manipulation. The recorded counts for the three imitation-learning tasks yield a pooled success rate of 82.7\% (124/150), compared with 62.7\% (94/150) using domain randomization alone. This pooled subtask result does not measure complete-workflow reliability or volumetric accuracy. The framework provides a basis for integrating planning and learned manipulation in laboratory workflows; further validation is needed for experiment-quality metrics and autonomous recovery.
\end{abstract}
''',r'''
\begin{abstract}
实验室液体操作包含容器运输、接触密集型抓取以及依赖示教的精细操作，不同环节具有不同的控制需求，难以通过单一策略统一处理。本文提出一种数字孪生辅助的混合机器人框架：采用约束运动规划执行运输，采用姿态感知强化学习执行抓取，并采用结合真实示教微调的模仿学习完成移液与滴加。Isaac Sim仿真环境用于支持策略训练，分层状态机用于协调可复用技能。评估范围包括导航、直立抓取、试剂移液、液滴滴加及梯度稀释相关操作。三个模仿学习子任务的记录计数汇总成功率为82.7\%（124/150），仅使用域随机化时为62.7\%（94/150）。这一汇总指标不代表完整工作流可靠性或液体体积精度。该框架为实验室工作流中的规划与学习控制集成提供了基础，实验质量指标和自主恢复能力仍需进一步验证。
\end{abstract}
''')

section('introduction',r'''
\section{Introduction}
\label{sec:introduction}
Automating laboratory liquid handling requires reliable interaction with containers, instruments, and spatially separated workstations. Transport should limit abrupt motion, grasping must maintain a suitable container orientation, and pipetting or dispensing requires consistent alignment. A robot may complete a motion sequence without achieving the required volume or dilution ratio; manipulation success and experimental quality must therefore be evaluated separately.

Mobile laboratory robots have demonstrated the feasibility of operating existing laboratory equipment \cite{burger2020mobile}. However, deploying a workflow still requires task-specific integration of perception, control, and execution monitoring. For the tasks considered here, a useful design question is how to assign predictable transport motions and contact-sensitive manipulations to complementary controllers, and how to coordinate them through explicit execution conditions.

We investigate a digital twin-assisted hybrid architecture. Classical planning addresses container transport, posture-aware proximal policy optimization (PPO) addresses grasping, and behavioral cloning with real-world fine-tuning addresses pipetting and dispensing. A hierarchical state machine (HSM) sequences these skills. The present scope is laboratory liquid handling: the reported subtask counts do not establish thin-film synthesis quality, corrosion resistance, or biological assay validity.

The contributions are: (1) an integrated planning-and-learning architecture with explicit task allocation; (2) a simulation-based grasping and imitation-learning pipeline with posture-related reward design and real-world adaptation; and (3) a subtask evaluation that distinguishes transport, grasping, and liquid-handling execution. The contribution is the application-specific integration and evaluation of these components, rather than a new PPO algorithm or a demonstrated learned high-level controller.

\revisionnote{Confirm the physical configuration before submission. Earlier sections describe Panda, a mobile tray, and a fixed UR3, whereas the experimental setup describes a mobile UR3. Associate each experiment with its actual robot and controller.}
''',r'''
\section{引言}
\label{sec:introduction}
实验室液体操作自动化要求机器人可靠地与容器、仪器及空间分布的工作站交互。运输过程需要限制运动突变，抓取过程需要维持适当的容器姿态，移液和滴加则要求稳定的定位与对准。机器人完成动作序列并不意味着体积或稀释比例满足实验要求，因此需要分别评估操作成功率和实验质量。

移动实验室机器人已展示操作现有实验设备的可行性\cite{burger2020mobile}。具体工作流的部署仍需要感知、控制和执行监测的任务适配。对于本文任务，核心问题是如何将可预测的运输动作与接触敏感操作分配给互补的控制器，并通过明确的执行条件协调各环节。

本文研究一种数字孪生辅助的混合架构：采用经典规划处理容器运输，采用姿态感知近端策略优化（PPO）处理抓取，采用结合真实示教微调的行为克隆处理移液和滴加，使用分层状态机（HSM）编排技能。当前研究范围限定为实验室液体操作，所报告的子任务计数不足以验证薄膜合成质量、防腐性能或生物化验有效性。

本文的贡献包括：（1）具有明确任务分工的规划与学习集成架构；（2）包含姿态奖励设计与真实世界适配的仿真抓取和模仿学习管线；（3）区分运输、抓取和液体操作执行效果的子任务评估。贡献重点是面向应用的系统集成与验证，而不是新的PPO算法，也不将尚未验证的高层学习控制作为已有成果。

\revisionnote{投稿前需确认真实硬件配置：原摘要描述Panda、移动托盘和固定UR3，原实验配置描述移动UR3。请将各项实验对应到实际机器人与控制器。}
''')

section('related_work',r'''
\section{Related Work}
\label{sec:related_work}
\subsection{Laboratory Automation}
Burger et al. demonstrated a mobile robotic chemist operating laboratory equipment \cite{burger2020mobile}. This motivates integrating robot operation with existing instruments. Our study concerns the execution layer of liquid-handling tasks; it does not evaluate autonomous scientific hypothesis selection or materials discovery. A comparison should distinguish the number of platforms, supported tasks, physical evaluation conditions, and measured experimental outcomes rather than characterize all prior systems as rigid waypoint executors.

\subsection{Simulation and Robot Learning}
Isaac Gym established GPU-based parallel simulation for robot learning \cite{makoviychuk2021isaac}. Isaac Sim and the Isaac Lab learning framework are distinct software components \cite{isaaclabdocs}. The actual simulator version and training framework should be reported for reproducibility. Parallel simulation supports collecting experience, but simulator fidelity and transfer performance require physical validation.

PPO is a policy optimization algorithm \cite{schulman2017ppo}; behavioral cloning learns from demonstrations. Mandlekar et al. examined the effects of datasets and learning choices in offline demonstration-based manipulation \cite{mandlekar2021matters}. Our framework combines these established approaches with task-specific control and real-world fine-tuning. Comparisons with additive orientation penalties and unregularized fine-tuning are needed to isolate the contribution of the proposed reward and adaptation choices.

\subsection{Transport and Skill Coordination}
Geometric path planning, trajectory timing, and execution monitoring address different aspects of transport. RRT* is sampling-based, whereas A* is graph-search based. A collision-free geometric path alone does not specify container acceleration or liquid motion. Likewise, coordinating learned low-level skills with a rule-based HSM should be distinguished from training a high-level reinforcement-learning policy. The present description uses HSM-based coordination; a learned scheduler and quantified recovery performance remain outside the demonstrated scope.
''',r'''
\section{相关工作}
\label{sec:related_work}
\subsection{实验室自动化}
Burger等展示了操作实验设备的移动机器人化学家\cite{burger2020mobile}，为机器人与现有仪器集成提供了依据。本文关注液体操作任务的执行层，不评估自主科学假设选择或材料发现。与现有系统比较时，应区分平台数量、任务范围、真实实验条件和实验质量指标，而不将已有系统统一描述为僵化的路点执行器。

\subsection{仿真与机器人学习}
Isaac Gym展示了面向机器人学习的GPU并行仿真\cite{makoviychuk2021isaac}。Isaac Sim与Isaac Lab学习框架属于不同的软件组件\cite{isaaclabdocs}，应报告实际使用版本及训练框架以支持复现。并行仿真能够支持经验采集，但仿真保真度与迁移效果仍需真实实验验证。

PPO是一种策略优化算法\cite{schulman2017ppo}，行为克隆则从示教中学习。Mandlekar等研究了离线示教数据及学习配置对机器人操作的影响\cite{mandlekar2021matters}。本文将这些已有方法与任务控制及真实示教微调结合。仍需与加性姿态惩罚及无正则微调进行比较，才能分离奖励设计和适配机制的具体贡献。

\subsection{运输与技能协调}
几何路径规划、轨迹时间参数化和执行监测分别处理运输中的不同问题。RRT*属于采样规划，A*属于图搜索。几何路径无碰撞本身并不规定容器加速度或液体运动。类似地，基于规则的HSM调用学习技能，应与通过强化学习训练高层策略区分。本文采用HSM技能协调的描述，学习型调度器及定量故障恢复性能不属于当前已验证范围。
''')

reward = r'''
\begin{align}
 M &= \operatorname{clip}(\mathbf{z}_{\rm curr}^{\mathsf T}\mathbf{z}_{\rm target},0,1),\\
 r_t &= -\alpha_1 d_t M + \alpha_2\mathbb{I}_{\rm grasp}M\nonumber\\
     &\quad +\alpha_3(h_t-h_0)M-\alpha_4\mathbb{I}_{\rm collision}.
\end{align}
'''
candidate = r'''
\begin{align}
 \theta_t &= \arccos\!\left(\operatorname{clip}\!\left(
 (\mathbf{R}_{obj,t}\mathbf{e}_{b})^{\mathsf T}\mathbf{e}_{z},-1,1\right)\right),\\
 r_t^{\rm candidate} &= w_d(d_{t-1}-d_t)+w_g\mathbb{I}_{\rm grasp}\nonumber\\
 &\quad +w_h(h_t-h_{t-1})-w_\theta\theta_t^2
 -w_c\mathbb{I}_{\rm collision}.
\end{align}
'''
mdp = r'''
\begin{align}
 o_t&=[\mathbf q_t,\dot{\mathbf q}_t,\mathbf p_{ee,t},\mathbf R_{ee,t},
 \hat{\mathbf p}_{obj,t},\hat{\mathbf R}_{obj,t},g_t],\\
 a_t&=[\mathbf u_t,u_{g,t}]\in\mathbb R^{d+1}.
\end{align}
'''
ppo = r'''
\begin{align}
 \rho_t(\theta)&=\frac{\pi_\theta(a_t|o_t)}{\pi_{\theta_{old}}(a_t|o_t)},\\
 L^{\rm clip}&=\hat{\mathbb E}_t[\min(\rho_t\hat A_t,
 \operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)\hat A_t)],\\
 \mathcal L_{\rm PPO}&=-L^{\rm clip}+c_v\mathcal L_V-c_e\mathcal H.
\end{align}
'''
bc = r'''
\begin{align}
 \mathcal L_{\rm BC}(\theta)&=\mathbb E_{(o,a)\sim\mathcal D_{sim}}
 [\|\mu_\theta(o)-a\|_2^2],\\
 \mathcal L_{\rm adapt}(\theta)&=\mathbb E_{(o,a)\sim\mathcal D_{real}}
 [\|\mu_\theta(o)-a\|_2^2]\nonumber\\
 &\quad+\lambda_{reg}\|\theta-\theta_{sim}\|_2^2.
\end{align}
'''

def table(text,label):
    for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}',text,re.S):
        if '\\label{'+label+'}' in m.group(): return m.group()
    raise ValueError(label)

men=r'''
\section{System Architecture and Methodology}
\label{sec:methodology}
\subsection{Task Allocation and Simulation}
\label{subsec:dt_construction}
The framework assigns transport to classical planning, grasping to PPO, and pipetting and dispensing to imitation learning. An HSM selects and monitors the active skill. Isaac Sim provides the virtual workspace for training, including robot and labware geometry and rigid-body contact parameters. SDF collision representations approximate contact geometry; they do not establish penetration-free behavior or fluid fidelity.
\begin{figure}[!t]
\centering\includegraphics[width=\linewidth]{images/Framework.png}
\caption{Existing framework illustration for the planning and learning pipeline. Platform assignments and embedded labels require consistency checks against the final hardware configuration.}
\label{fig:overall_framework}
\end{figure}
\revisionnote{Record simulator and learning-library versions, robot assets, simulation time step, contact settings, calibration errors, and the direction and frequency of real--virtual updates. Fluid simulation and validated fluid parameters have not been established by the supplied text.}

\subsection{Transport Planning}
\label{subsec:macro_planning}
The draft transport objective penalizes the squared third derivative of a trajectory over a fixed duration. Container roll and pitch are bounded during transport. These are motion-smoothing and orientation requirements, rather than a proof of spill-free motion.
\begin{equation}
\min_{q(\cdot)}\int_0^T\|\dddot q(t)\|^2dt,
\quad |\phi-\phi_{target}|\le\epsilon_\phi,
\quad |\vartheta-\vartheta_{target}|\le\epsilon_\vartheta.
\end{equation}
\revisionnote{Confirm what $q$ represents in the implementation: arm joints, base coordinates, or container position. Specify velocity and acceleration bounds, fixed duration or time penalty, boundary conditions, collision constraints, and differential-drive feasibility. Mixed angular and linear coordinates require explicit weighting. Container geometry, fill ratio, and acceleration limits must be reported before discussing liquid stability.}

\subsection{Grasping Observations and Actions}
\label{subsec:arm_rl}
Grasping is optimized as a sequential decision problem. We distinguish measured observations from complete simulator state:
'''+mdp+r'''
Here $d$ is the arm's number of joints (six for UR3 and seven for Panda), and hats denote estimated object poses. $\mathbf u_t$ represents the arm command and $u_{g,t}$ the gripper command. The chosen orientation encoding determines the numerical input dimension.
\revisionnote{Identify the robot used for each policy, whether commands are position increments or velocities, action scaling and control frequency, object-pose estimation, and the gripper observation. Specify whether the actor receives privileged simulator state and how real observations replace it.}

\subsubsection{Posture Reward: Implementation Check}
\label{subsec:reward_design}
The previous draft specifies the following reward, with $d_t$ the approach distance and $h_t$ the object height:
'''+reward+r'''
This expression is retained for traceability, not endorsed as a corrected implementation. Multiplying a negative distance penalty by $M$ reduces that penalty when $M$ approaches zero. Therefore, $M=0$ is not itself a strong orientation penalty. The original downward target axis also requires checking against the object's local axis convention.
\revisionnote{Compare the expressions with the training code before interpreting the existing reward ablation. The sensitivity parameter $\alpha_{posture}$ is absent from the recorded reward and must be recovered from the actual configuration.}

A candidate correction separates approach progress and orientation cost:
'''+candidate+r'''
Here $\mathbf e_b$ points from the bottle base toward its opening in the object frame, and $\mathbf e_z$ is the world upward direction. This definition constrains the bottle rather than the gripper approach axis. The candidate is a revision proposal; no existing result is attributed to it. Adopting it requires retraining and evaluation, including reward scaling and terminal conditions.

\subsubsection{PPO and Randomization}
\label{subsec:ppo}
PPO \cite{schulman2017ppo} uses the likelihood ratio and minimized loss:
'''+ppo+r'''
The original training settings are retained below. They require a matching run configuration, rollout length, network architecture, terminal-state treatment, and random seeds.
'''+table(old['methodology'],'tab:hyperparameters')+r'''
\label{subsec:domain_randomization}
Each randomized parameter is sampled as $\xi_i\sim\mathcal U(l_i,u_i)$ using the listed bounds. This notation allows asymmetric intervals around the nominal value.
'''+table(old['methodology'],'tab:domain_randomization')+r'''
\revisionnote{Document which randomizations affect RL observations and which affect IL images. State-only policies do not directly benefit from lighting changes unless the perception pipeline supplies their observations.}

\subsection{Imitation Learning and Adaptation}
\label{subsec:arm_il_adaptation}
The draft uses SpaceMouse demonstrations in simulation and $M$ physical demonstration trajectories for adaptation. With predicted action mean $\mu_\theta(o)$, the objectives are:
'''+bc+r'''
The regularizer limits parameter displacement from the simulation policy. Its independent benefit requires comparison with unregularized fine-tuning. The current description does not establish a causal correction of refraction, surface tension, or gripper compliance.
\revisionnote{Supply image and proprioceptive inputs, action units and normalization, network architecture, simulated demonstration count, whether $M=10$ is per task or shared, adaptation epochs and $\lambda_{reg}$. Keep evaluation trials separate from demonstrations.}

\subsection{HSM-Based Skill Coordination}
\label{subsec:hierarchical_skill}
A skill interface comprises its input observations, controller, entry conditions, termination conditions, timeout, and outcome status. Transport may call a classical controller, whereas manipulation calls a learned policy. The HSM selects a skill from the current workflow state and observations; this does not require a learned high-level policy. Independently stored policies avoid direct overwriting of one skill's parameters when another is updated, but this is not a demonstrated continual-learning result.

Recovery should be conditional on a valid, reachable object pose and intact labware. A lost-grasp signal alone is insufficient to justify an automatic regrasp. Recovery rules, retry limits, and intervention counts require implementation-specific documentation and evaluation.

\subsection{Proposed Multi-Platform Extension}
\label{subsec:handover}
The earlier design proposes a Panda workstation, a mobile transport tray, and a UR3 workstation, with fiducial localization and docking confirmation for container handover. This extension is retained as a design direction, not as an experimentally validated contribution. The sensor type, frame transforms, localization accuracy, grasp verification logic, and fault handling must be established before quantitative handover claims are made. An average force threshold alone does not establish continuous secure contact throughout a time window.
'''
mzh=r'''
\section{系统架构与方法}
\label{sec:methodology}
\subsection{任务分工与仿真}
\label{subsec:dt_construction}
框架将运输分配给经典规划，将抓取分配给PPO，将移液与滴加分配给模仿学习，由HSM选择并监测当前技能。Isaac Sim提供训练所用的虚拟工作空间，包含机器人、器材几何及刚体接触参数。SDF碰撞表示用于近似接触几何，但本身不能证明无穿透或流体仿真保真度。
\begin{figure}[!t]
\centering\includegraphics[width=\linewidth]{images/Framework.png}
\caption{已有规划与学习框架示意图。平台分工及图内标注仍需与最终硬件配置核对。}
\label{fig:overall_framework}
\end{figure}
\revisionnote{补充仿真器与学习库版本、机器人资产、仿真步长、接触参数、标定误差及虚实更新的方向与频率。现有文字尚不足以确认流体仿真实现及其参数验证。}

\subsection{运输规划}
\label{subsec:macro_planning}
原稿运输目标在固定时长内最小化轨迹三阶导数的平方积分，并约束容器横滚与俯仰。这些条件用于轨迹平滑和姿态限制，不构成无洒液的证明。
\begin{equation}
\min_{q(\cdot)}\int_0^T\|\dddot q(t)\|^2dt,
\quad |\phi-\phi_{target}|\le\epsilon_\phi,
\quad |\vartheta-\vartheta_{target}|\le\epsilon_\vartheta.
\end{equation}
\revisionnote{根据实现确认$q$代表机械臂关节、底盘坐标还是容器位置；补充速度与加速度界、固定时长或时间代价、边界条件、碰撞约束及差速运动可行性。角度和长度坐标混合时需明确权重。讨论液体稳定性前需报告容器几何、装液比例和加速度限制。}

\subsection{抓取观测与动作}
\label{subsec:arm_rl}
将抓取视为序贯决策问题，并区分可测观测与完整仿真状态：
'''+mdp+r'''
其中$d$为机械臂关节数，UR3为6，Panda为7；带帽变量为物体位姿估计。$\mathbf u_t$为机械臂控制指令，$u_{g,t}$为夹爪指令。姿态的具体编码决定网络输入维度。
\revisionnote{确认各策略所用机器人、位置增量或速度控制方式、动作缩放与控制频率、物体位姿估计及夹爪观测；说明执行策略是否使用仿真特权状态，以及真实部署时如何替换这些输入。}

\subsubsection{姿态奖励：实现核对}
\label{subsec:reward_design}
原稿记录的奖励如下，其中$d_t$为接近距离，$h_t$为物体高度：
'''+reward+r'''
保留此式用于追溯，不将其视为已修正实现。负距离惩罚乘以$M$后，在$M$趋近零时惩罚反而减小，因此$M=0$本身不构成强姿态惩罚。原稿向下目标轴也需与物体局部坐标约定核对。
\revisionnote{解释已有奖励消融前，必须对照训练代码核实公式。敏感性参数$\alpha_{posture}$未出现在原奖励中，需要从真实配置恢复其定义。}

可考虑将接近进展和姿态代价分离，候选修改为：
'''+candidate+r'''
其中$\mathbf e_b$在物体坐标系中由瓶底指向瓶口，$\mathbf e_z$为世界坐标系向上方向。该定义约束瓶体，而非夹爪接近轴。此式仅为修改候选，不对应已有实验结果；若采用，需要重新训练与评估，并确定奖励尺度及终止条件。

\subsubsection{PPO与域随机化}
\label{subsec:ppo}
PPO\cite{schulman2017ppo}采用以下似然比与最小化损失：
'''+ppo+r'''
下表保留原稿训练设置，仍需对应运行配置、采样轨迹长度、网络结构、终止状态处理和随机种子。
'''+table(old['methodology_chinese'],'tab:hyperparameters')+r'''
\label{subsec:domain_randomization}
各随机参数按$\xi_i\sim\mathcal U(l_i,u_i)$从表列区间采样，该表示允许名义值两侧的区间不对称。
'''+table(old['methodology_chinese'],'tab:domain_randomization')+r'''
\revisionnote{区分影响RL观测的随机化与影响IL图像的随机化。若RL只接收状态，光照变化只有通过感知管线影响观测时才可能直接影响该策略。}

\subsection{模仿学习与适配}
\label{subsec:arm_il_adaptation}
原稿使用SpaceMouse采集仿真示教，并用$M$条真实示教轨迹进行适配。以$\mu_\theta(o)$表示动作预测均值，目标函数为：
'''+bc+r'''
正则项限制参数相对仿真策略的偏移，其独立收益需要与无正则微调比较。现有描述不能证明该方法分别修正了折射、表面张力或夹爪柔顺性误差。
\revisionnote{补充图像与本体感知输入、动作单位及归一化、网络架构、仿真示教数量、$M=10$是否按任务分别统计、微调轮数和$\lambda_{reg}$。测试试验与训练示教应独立。}

\subsection{基于HSM的技能协调}
\label{subsec:hierarchical_skill}
技能接口包含输入观测、控制器、进入条件、终止条件、超时和结果状态。运输技能可调用经典控制器，操作技能调用学习策略。HSM根据工作流状态和观测选择技能，不要求学习高层策略。独立存储策略可以避免更新一个技能时直接覆盖另一个技能参数，但不构成已验证的持续学习结果。

故障恢复应以物体位姿有效、位置可达及器材完好为前提，不能仅凭失去抓取信号就自动重新抓取。恢复规则、重试上限及人工干预次数需依据实现补充并评估。

\subsection{多平台扩展设计}
\label{subsec:handover}
原设计提出Panda工作站、移动运输托盘与UR3工作站，利用视觉标记定位及停靠确认支持容器交接。这里将其保留为扩展方向，不作为已获实验验证的贡献。定量评价前需确认传感器类型、坐标变换、定位精度、抓取验证逻辑及故障处理。平均力阈值本身不能证明整个时间窗口内持续可靠接触。
'''
section('methodology',men,mzh)

def wilson(k,n):
    p=k/n; z=1.96; den=1+z*z/n
    c=(p+z*z/(2*n))/den
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return f'{100*(c-h):.1f}--{100*(c+h):.1f}'

wilson_eq=r'''
\begin{equation}
 [p_L,p_U]=\frac{\hat p+z^2/(2n)\ \pm\ z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n},
 \quad z=1.96.
\end{equation}
'''

blocks=[
('navigation_metrics','Transport','运输',
'The retained counts are 37/50, 34/50, and 44/50. They describe navigation outcomes under the original test conditions. The table does not directly measure liquid mass loss. Planning time must distinguish complete path generation from policy inference, and the clearance comparison requires matched scenes and start--goal pairs.',
'保留计数分别为37/50、34/50和44/50，表示原测试条件下的导航结果。该表未直接测量液体质量损失。规划时间需区分完整路径生成与策略推理，间距比较需使用匹配的场景与起终点。'),
('rl_grasping','Grasping','抓取',
'The recorded grasp success counts are 158/200 and 172/200. The reported tilt statistic must be defined as, for example, the mean of per-trial peak angles, with the meaning of the spread specified. Zero recorded spillage is an observation under the tested conditions, not a zero-risk guarantee.',
'原记录抓取成功次数为158/200和172/200。倾角统计需明确，例如各试次峰值角度的均值，并说明离散量的含义。记录中零洒液只表示测试条件下的观察结果，不能推断风险为零。'),
('sensitivity','Posture Sensitivity','姿态敏感性',
'The entry 170/200 has been corrected to 85.0 percent. The parameter definition must be recovered from the training configuration before this table can establish a reward-design effect. Its zero-weight condition differs from the preceding baseline and needs a run-level explanation.',
'170/200对应的百分比已更正为85.0。必须从训练配置补充权重定义后，才能据此分析奖励设计效果。零权重条件与前表基线结果不同，需要依据运行记录解释。'),
('parallel_envs','Parallel Training','并行训练',
'The recorded wall times yield a 12.5/1.8, or approximately 6.9-fold, reduction from 256 to 4096 environments. This is not by itself evidence of improved sample efficiency. Report total transitions, rollout length, seed variation, hardware, rendering settings, and the convergence criterion.',
'原记录中256与4096环境的训练耗时比为12.5/1.8，约6.9倍，但该结果本身不证明样本效率提升。需补充总交互步数、采样长度、种子差异、硬件、渲染配置和收敛判据。'),
('il_manipulation','Imitation-Learning Transfer','模仿学习迁移',
'The three equally sized subtask groups yield pooled counts of 43/150, 94/150, and 124/150 for vanilla BC, domain randomization, and domain randomization plus fine-tuning. The corresponding rates are 28.7, 62.7, and 82.7 percent. This comparison evaluates the combined adaptation pipeline; without unregularized fine-tuning it cannot isolate the regularizer. A pooled subtask rate is not a complete-workflow rate or a volume-accuracy measurement.',
'三个等规模子任务组的汇总计数为43/150、94/150和124/150，分别对应普通BC、域随机化、域随机化加微调，成功率为28.7、62.7和82.7个百分点。该比较评估联合适配管线，没有无正则微调对照时不能分离正则项贡献。汇总子任务成功率不等于全流程成功率或体积精度。'),
('few_shot','Demonstration Count','示教数量',
'The recorded count improves from 31/50 without real demonstrations to 42/50 with ten demonstrations. Identify the task and data split; the zero-demonstration row differs from the pipetting DR-only row above. The difference between 42/50 and 43/50 does not establish a universal saturation point at ten demonstrations.',
'记录成功次数从无真实示教时31/50提高到十条示教时42/50。需注明任务及数据划分，无示教行与上表移液DR-only结果不同。42/50与43/50的差异不能证明十条示教是普适的性能饱和点。'),
]

for zh in [False,True]:
    src=old['experiments_chinese' if zh else 'experiments']
    exp=(r'\section{实验与结果}' if zh else r'\section{Experiments and Results}')+'\n'+r'\label{sec:experiments}'+'\n'
    exp+=(r'\revisionnote{本修订保留原稿主要表格计数，未验证原始日志。所有结果解释均以确认数据来源、成功判据、测试批次与训练配置为前提。}' if zh else r'\revisionnote{The principal table counts are retained from the previous draft; raw logs have not been verified. Interpretation requires confirmation of provenance, success criteria, test cohorts, and training configurations.}')+'\n'
    exp+=(r'对于单项二元结果，按成功次数$k$与试验次数$n$计算$\hat p=k/n$，采用Wilson 95\%区间\cite{nistwilson}：' if zh else r'For an individual binary outcome, let $\hat p=k/n$ for $k$ successes in $n$ trials. We use the Wilson 95\% interval \cite{nistwilson}:')+wilson_eq
    exp+=(r'下方区间表由原计数计算，假定同一条件内试次独立且成功概率固定，不包含训练随机种子或跨任务异质性造成的不确定性。跨任务汇总仅作为描述性统计，不强行赋予单一二项分布区间。' if zh else 'The interval table below is calculated from the recorded counts, assuming independent trials with a fixed success probability within each condition. It excludes uncertainty across training seeds or heterogeneous tasks. Cross-task pooling is descriptive and is not assigned a single binomial interval.')+'\n'
    exp+=(r'\subsection{硬件配置与测试条件}' if zh else r'\subsection{Hardware and Test Conditions}')+'\n'+r'\label{subsec:exp_setup}'+'\n'
    exp+=(r'原实验配置列出UR3、Robotiq 2F-85、RealSense D435、差速底盘及RTX 4090工作站，但尚需核对机械臂是否搭载于底盘，以及Panda参与哪些试验。' if zh else 'The original setup lists a UR3, Robotiq 2F-85, RealSense D435, differential-drive base, and RTX 4090 workstation. Whether the arm is base-mounted, and which trials involve a Panda, must be reconciled with the hardware record.')+'\n'
    exp+=(r'\revisionnote{补充容器尺寸、材质、装液比例、液体类型、目标体积、姿态与位置扰动、成功判据、超时、失败及重试计数、测试是否为真机，以及多随机种子训练设置。}' if zh else r'\revisionnote{Supply container geometry, material, fill ratio, liquid type, target volume, pose perturbations, success criteria, timeout, failure and retry counts, whether each evaluation is physical, and training-seed settings.}')+'\n'
    for label,en_title,zh_title,en_para,zh_para in blocks:
        exp+='\n\\subsection{'+(zh_title if zh else en_title)+'}\n'
        t=table(src,'tab:'+label)
        t=t.replace('170 & 84.8','170 & 85.0')
        if label=='navigation_metrics':
            t=t.replace('Mean Trajectory Jerk ($m/s^3$)','Jerk (definition pending)').replace('平均轨迹冲击 ($m/s^3$)','jerk（定义待核实）')
        exp+=t+'\n'+(zh_para if zh else en_para)+'\n'
        if label=='navigation_metrics':
            exp+=(r'\revisionnote{原jerk公式为关节三阶导数的平方均值，与$m/s^3$单位不一致。暂保留数值以便追溯，不据此宣称洒液改善。根据原轨迹确认是均值模长、均方还是均方根，并统一坐标、单位、采样与滤波方法。}' if zh else r'\revisionnote{The original jerk formula is a mean squared joint derivative, inconsistent with the reported $m/s^3$ unit. Values are retained for traceability, without a spillage inference. Recover the actual metric, coordinate frame, units, sampling, and filtering from trajectory logs.}')+'\n'
    exp+='\n\\subsection{'+('单条件成功率区间' if zh else 'Per-Condition Success Intervals')+'}\n'
    exp+=r'\begin{table}[!t]\centering'+'\n'+r'\caption{'+('由原计数重算的Wilson 95\%区间（百分比）' if zh else 'Wilson 95\% intervals recalculated from retained counts (percent)')+'}\n'+r'\label{tab:verified_intervals}'+'\n'+r'\begin{tabular}{lcc}\hline'+'\n'
    exp+=('条件 & 成功/试验 & 区间' if zh else 'Condition & Successes/trials & Interval')+r'\\\hline'+'\n'
    for en,cn,k,n in [('RRT*','RRT*',37,50),('DRL navigation','DRL导航',34,50),('Proposed transport','本文运输',44,50),('Baseline PPO','基线PPO',158,200),('Posture PPO','姿态PPO',172,200),('Adapted pipetting','微调移液',42,50),('Adapted dispensing','微调滴加',40,50),('Adapted dilution','微调稀释',42,50)]:
        exp+=(cn if zh else en)+f' & {k}/{n} & {wilson(k,n)}'+r'\\'+'\n'
    exp+=r'\hline\end{tabular}\end{table}'+'\n'
    exp+='\n\\subsection{'+('全流程统计边界' if zh else 'Limits of Workflow-Level Reporting')+'}\n'+r'\label{subsec:exp_end_to_end}'+'\n'
    exp+=(r'原稿全流程表记录42/50成功，而其中接触角阶段记录40/50成功。若来自同一批试验且全流程要求每一步首次成功，这两项计数不相容。允许重试或采用不同批次可以解释差异，但必须通过原始记录确认。因此，本修订不将该表作为全流程可靠性的证据。原稿及计数已保存于修订备份。' if zh else 'The original workflow table reports 42/50 complete successes but only 40/50 successes at the contact-angle stage. These counts are incompatible if they refer to the same cohort and require first-attempt success at every stage. Retries or different cohorts could explain the discrepancy, but must be confirmed from records. The table is therefore withheld as evidence of full-workflow reliability; its original values remain in the revision backup.')+'\n'
    exp+=(r'\revisionnote{核对完整试次编号、各阶段首次结果、重试次数、最终结果及人工干预，并解释“连续完成10次”与50次试验的关系。完成核对后分别报告首次全流程成功率、重试后成功率和耗时。}' if zh else r'\revisionnote{Reconcile trial IDs, first-attempt stage outcomes, retries, final outcomes, and interventions, including the relationship between ten consecutive completions and fifty trials. Then report first-attempt and retry-assisted workflow success separately.}')+'\n'
    exp+='\n\\subsection{'+('实验质量与补充验证' if zh else 'Experiment Quality and Additional Validation')+'}\n'
    exp+=(r'后续验证应测量移液体积误差与重复性、稀释比例误差及其逐级累积、接触角测量重复性，并以匹配条件下的人工或传统自动化操作作为参考。薄膜制备与跨平台交接在获得真实结果前仅作为扩展计划。抓取需增加经典控制和加性姿态惩罚对照；迁移需增加无正则微调对照。已有表格不能替代上述质量评估。' if zh else 'Further validation should measure pipetting volume error and repeatability, dilution-ratio error and accumulation, and contact-angle repeatability against matched manual or conventional automation references. Thin-film fabrication and multi-platform handover remain extensions until physical evidence is available. Grasping requires classical-control and additive-posture baselines; adaptation requires an unregularized fine-tuning baseline. Existing execution tables do not replace these quality measurements.')+'\n'
    # Scale only tables that exceed a narrow two-column layout; preserve existing wrappers.
    exp=re.sub(r'\\begin\{table\}.*?\\end\{table\}',lambda m: m.group() if '\\resizebox' in m.group() else m.group().replace('\\begin{tabular}',r'\resizebox{\columnwidth}{!}{'+'\n'+r'\begin{tabular}',1).replace('\\end{tabular}',r'\end{tabular}}',1),exp,flags=re.S)
    write('sections/experiments'+('_chinese' if zh else '')+'.tex',exp)

section('conclusion',r'''
\section{Conclusion and Limitations}
\label{sec:conclusion}
This work describes a digital twin-assisted hybrid approach to laboratory liquid handling, combining classical transport planning, reinforcement-learning grasping, imitation-learning manipulation, and HSM-based coordination. The retained IL counts indicate 124 successes in 150 subtask trials after domain randomization and real-world fine-tuning. This is a pooled execution statistic and does not establish complete-workflow reliability or experimental accuracy.

The present revision identifies unresolved hardware, reward-implementation, and evaluation-protocol details. Liquid stability is not guaranteed by trajectory smoothing alone. The individual benefit of regularization, physical model fidelity, and autonomous recovery requires controlled evaluation. Future work should first establish volumetric and dilution quality, reproducible training configurations, and reconciled workflow logs. Multi-platform handover, thin-film processing, and language-guided planning are subsequent extensions rather than conclusions of the current evaluation.
''',r'''
\section{结论与局限}
\label{sec:conclusion}
本文描述了一种数字孪生辅助的实验室液体操作混合方法，将经典运输规划、强化学习抓取、模仿学习操作和HSM协调结合。保留的IL计数表明，域随机化与真实示教微调后，150次子任务试验中有124次成功。该结果属于汇总执行统计，不代表完整工作流可靠性或实验精度。

当前修订明确列出了尚待核实的硬件、奖励实现和评估协议细节。单纯轨迹平滑不能保证液体稳定，正则项独立收益、物理模型保真度与自主恢复能力需要受控实验验证。后续应优先补充体积与稀释质量、可复现训练配置及一致的全流程日志。多平台交接、薄膜加工和语言引导规划属于后续扩展，而非当前评估已经证明的结论。
''')

bibliography=r'''
\begin{thebibliography}{99}
\bibitem{burger2020mobile} B. Burger \textit{et al.}, ``A mobile robotic chemist,'' \textit{Nature}, vol. 583, pp. 237--241, 2020, doi: 10.1038/s41586-020-2442-2.
\bibitem{makoviychuk2021isaac} V. Makoviychuk \textit{et al.}, ``Isaac Gym: High performance GPU-based physics simulation for robot learning,'' arXiv:2108.10470, 2021.
\bibitem{isaaclabdocs} NVIDIA, ``Isaac Lab,'' \textit{Isaac Sim Documentation}, ver. 5.0.0. [Online]. Available: \url{https://docs.isaacsim.omniverse.nvidia.com/5.0.0/isaac_lab_tutorials/index.html}. Accessed: Sep. 6, 2026.
\bibitem{schulman2017ppo} J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, ``Proximal policy optimization algorithms,'' arXiv:1707.06347, 2017.
\bibitem{mandlekar2021matters} A. Mandlekar \textit{et al.}, ``What matters in learning from offline human demonstrations for robot manipulation,'' in \textit{Proceedings of the 5th Conference on Robot Learning}, PMLR, vol. 164, pp. 1678--1690, 2022.
\bibitem{nistwilson} NIST/SEMATECH, ``Confidence intervals,'' \textit{e-Handbook of Statistical Methods}, sec. 7.2.4.1. [Online]. Available: \url{https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm}. Accessed: Sep. 6, 2026.
\end{thebibliography}
'''
write('sections/bibliography.tex',bibliography)
for zh in [False,True]:
    main=r'''\documentclass[journal,twocolumn]{IEEEtran}
\usepackage{graphicx}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb,booktabs}
\usepackage{cite}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\setCJKmainfont{SimSun}
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}
\newcommand{\revisionnote}[1]{\par\smallskip\noindent{\color{red!65!black}\small\textbf{'''+('待核实：' if zh else 'Author verification: ')+r'''}#1}\par\smallskip}
\begin{document}
\title{'''+('数字孪生辅助的实验室液体操作混合机器人框架' if zh else 'A Digital Twin-Assisted Hybrid Robotic Framework for Laboratory Liquid Handling')+r'''}
\author{cx guo}
\maketitle
'''
    for part in ['abstract','introduction','related_work','methodology','experiments','conclusion']:
        main+='\\input{sections/'+part+('_chinese' if zh else '')+'}\n'
    main+='\\input{sections/bibliography}\n\\end{document}\n'
    write('main_chinese.tex' if zh else 'main.tex',main)
    if not zh:
        standalone=re.sub(r'\\input\{([^}]+)\}',lambda m:(root/(m.group(1)+'.tex')).read_text(encoding='utf-8'),main)
        write('main_standalone.tex',standalone)

write('REVISION_NOTES.md',f'''# 论文修订说明

本次修改为可继续完善的审阅稿，不是已经核实实验数据的投稿终稿。

## 文件与备份

- 英文入口：main.tex；中文入口：main_chinese.tex。
- 单文件英文版：main_standalone.tex，已与分章节稿同步。
- 修改前源码与已有 PDF：{backup.name}/。
- 早期 panda_rl.tex 与工作区其他 PDF 未改动。

## 已完成

1. 标题与摘要聚焦实验室液体操作；将未验证的三平台交接、薄膜制备定位为扩展设计。
2. 将高层协调统一为 HSM，去掉概率元控制器已训练、消除遗忘等缺少支撑的结论。
3. 中英文统一方法范围；移出只有中文稿声称使用而缺少对应评估的 DAgger、GAIL、课程学习及冗长通用推导，原文保留在备份中。
4. 指出原奖励负项乘姿态因子的激励问题与轴定义问题；保留原式供对照，另列候选修正，明确候选没有对应实验。
5. 动作维度按关节数参数化，未擅自确定位置或速度控制；区分观测与仿真状态。
6. 修正 PPO 最小化损失符号及概率比命名；域随机化改用上下界表示。
7. 170/200 从84.8%改为85.0%；修正 Wilson 公式，新增8个单条件区间。区间假设独立二项试验，不代表多种子不确定性；跨任务汇总只作描述。
8. 82.7%限定为IL三子任务124/150汇总；不再称为全流程成功率。
9. 将有口径矛盾的全流程表撤出结论依据，但在正文解释42/50与40/50的冲突，备份保留全表。
10. jerk数值保留但单位与算法明确待核实；未任意转换数值或宣称洒液因果改善。
11. 移除空图、空结果章节及缺少结果的表格；原图只保留框架图并注明图内标签待确认。
12. 相关工作收缩为当前方法需要的可核实来源，所有正文引用与参考文献键对应。原扩展综述保留于备份，投稿前应进一步补充与真实贡献最接近的工作。

## 必须由实际记录解决的问题

- 硬件：UR3固定还是移动，Panda参与哪些实验？每种策略对应哪台机械臂？
- 奖励：轴方向、权重与代码一致吗？alpha_posture如何进入公式？若采用候选奖励，必须重训再报告。
- 数据：表格是否来自真实试验日志？不同表格的基线差异属于不同批次还是录入问题？
- 全流程：完整成功42/50与必要子步骤40/50如何对应？是否重试、不同批次或人工干预？连续10次的范围是什么？
- 统计：倾角的±是标准差还是区间？零洒液的分母包含失败抓取吗？每个成功判据是什么？
- 训练：配置、随机种子、rollout长度、总交互步数、输入输出、真实示教数量与数据划分。
- jerk：坐标、单位、模长/均方/均方根、采样和滤波；时间和碰撞约束。
- 实验质量：真实体积误差、稀释比例、重复性；浸涂与交接若保留为贡献需补真实实验。

正文深红色“待核实/Author verification”是可见作者标记；核实前不要直接删除标记并投稿。

## 来源

- https://www.nature.com/articles/s41586-020-2442-2
- https://arxiv.org/abs/2108.10470
- https://docs.isaacsim.omniverse.nvidia.com/5.0.0/isaac_lab_tutorials/index.html
- https://arxiv.org/abs/1707.06347
- https://proceedings.mlr.press/v164/mandlekar22a.html
- https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
''')
write('README.md',r'''# 数字孪生辅助的实验室液体操作混合机器人框架

当前版本为带可见作者核实标记的中英文修订稿，具体变化见 REVISION_NOTES.md。

- main.tex / main.pdf：英文分章节稿。
- main_chinese.tex / main_chinese.pdf：中文稿。
- main_standalone.tex / main_standalone.pdf：同步的单文件英文稿。
- sections/bibliography.tex：当前共用参考文献；references.bib 是旧占位文件，当前入口不使用。
- revision_backup_*：修订前源码与已有 PDF。

在本目录使用 XeLaTeX 连续编译两次，例如 `xelatex -interaction=nonstopmode -halt-on-error main.tex`。

82.7%来自原稿三个IL子任务的124/150计数，不代表已核实的全流程成功率。原始实验记录、硬件配置及奖励代码尚需作者确认。深红色核实标记解决后才能整理投稿版。
''')
print('Backup:',backup)
print('Revised bilingual sections and three manuscript entry points.')
