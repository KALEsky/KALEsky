# KALEsky

Hi, I’m KALEsky.

这里主要放我本科阶段真正写过、跑过、调过的实验和项目。它们有些很小，有些依赖已经过时的工具链，但放在一起之后，能看出我一直在追同一类问题：一段程序从源码到机器码会发生什么，数据怎样在系统里流动，算法换一种执行方式之后瓶颈又会跑到哪里。

## What I work on

- **Systems and low-level programming**：汇编、x86 启动过程、Linux 0.11、进程调度、Tiny Shell。
- **Compilers and programming languages**：Flex/Bison、AST、符号表、语义检查和中间代码优化。
- **Networks and distributed execution**：HTTP 代理、GBN/SR、IPv4 转发、Wireshark、MPI、PThread、OpenMP 和 CUDA。
- **Data and machine learning**：SQL/JDBC、缓冲区管理、拟合、逻辑回归、聚类、HMM、PCA 和图像处理。
- **Hardware experiments**：Verilog/Vivado FPGA 密码锁，以及在 RISC-V 环境上做过运行演示的项目。

## Selected projects

这些仓库按“打开后能不能比较快看懂、能不能看出我做过什么”来挑，不完全按时间排序：

1. [HIT-Bachelor-Thesis-Federated-Learning](https://github.com/KALEsky/HIT-Bachelor-Thesis-Federated-Learning) — 本科毕业设计：用 Shapley 值评估客户端贡献，并通过信誉加权聚合减轻恶意参与者的影响。
2. [HIT-Machine-Learning-Labs](https://github.com/KALEsky/HIT-Machine-Learning-Labs) — 从多项式拟合、逻辑回归到聚类和 PCA，记录了把公式自己写成实验的过程。
3. [HIT-Computer-Systems-Labs](https://github.com/KALEsky/HIT-Computer-Systems-Labs) — 数据表示、汇编、Bomb Lab、缓存友好优化和 Tiny Shell，比较集中地展示系统软件基础。
4. [HIT-Operating-Systems-Labs](https://github.com/KALEsky/HIT-Operating-Systems-Labs) — 从 `iret`、TSS、启动扇区到 Linux 0.11 系统调用和进程运行轨迹。
5. [HIT-Compiler-Labs](https://github.com/KALEsky/HIT-Compiler-Labs) — C-- 的词法/语法分析、符号表、语义检查和线性 IR 优化。
6. [HIT-Computer-Networks-Labs](https://github.com/KALEsky/HIT-Computer-Networks-Labs) — HTTP 缓存代理、可靠 UDP、IPv4 收发/转发和协议抓包分析。
7. [HIT-Parallel-Computing-Labs](https://github.com/KALEsky/HIT-Parallel-Computing-Labs) — MPI、PThread、OpenMP 和 CUDA 放在同一组实验里比较。
8. [HIT-RISC-V-Experiments](https://github.com/KALEsky/HIT-RISC-V-Experiments) — 浏览器里的 RISC-V/VDP 模拟器和面向自定义硬件的 bare-metal 固件，能把前端模拟、汇编启动代码和设备寄存器串起来看。

另外还有 [HIT-Database-Systems-Labs](https://github.com/KALEsky/HIT-Database-Systems-Labs) 和 [HIT-Digital-Logic-Password-Lock](https://github.com/KALEsky/HIT-Digital-Logic-Password-Lock)，一个往数据库引擎内部走，一个把同步逻辑落到 FPGA 上。

## Graduate coursework

研究生阶段的课程实验也单独整理成了三个仓库：

- [USTC-Deep-Learning-Labs](https://github.com/KALEsky/USTC-Deep-Learning-Labs) — 从 MLP、Tiny-ImageNet、Yelp RNN 到 GCN 节点分类和链接预测。
- [USTC-Algorithm-Design-Labs](https://github.com/KALEsky/USTC-Algorithm-Design-Labs) — 排序、树、动态规划、Huffman、回溯和图搜索。
- [USTC-Machine-Learning-Labs](https://github.com/KALEsky/USTC-Machine-Learning-Labs) — 表格数据特征工程、CatBoost，以及天气图像多任务分类。

## A note about these repositories

这些不是我临时拼出来的简历项目，而是把多年课程实验重新整理后上传的作品。每个仓库尽量保留源码、实验报告、结果图和当时的技术背景；同时把明显的本机路径、密码、私钥、生成物和来源不清的材料排除掉。

因此，有些仓库可以直接运行，有些需要旧版 Java、MindSpore、Flex/Bison、Bochs、Vivado 或 CUDA 环境。README 会把能验证的部分说清楚，也会把没有在现代环境复现的部分直接标出来。

## Tools I have used

`C/C++` · `Python` · `Java` · `SQL/MySQL` · `Verilog` · `JavaScript/Quick App` · `Flex/Bison` · `Linux 0.11` · `MPI` · `OpenMP` · `PThread` · `CUDA` · `MindSpore` · `Vivado`

## A small trail through the work

早期的项目更多是在学习怎么把一个想法跑起来：控制台游戏、JDBC 小程序、快应用和各种课程 Demo。后来实验开始向下分层——编译器把程序变成 AST/IR，操作系统实验开始看中断、任务和调度，计算机系统实验则继续追到缓存、进程组和信号。

机器学习和计算建模是另一条线：从拟合、分类和聚类，到 HMM、PCA、图像去噪和鲁棒拟合。现在回头看，这些题目不一定都大，但它们帮我形成了比较稳定的兴趣：喜欢把抽象算法放进一个能运行、能观察结果的具体系统里。

更多个人博客内容在 [KALEsky.github.io](https://kalesky.github.io/)。
