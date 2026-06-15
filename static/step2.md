# 进阶篇使用手册

**Claude-Haha / Claude Code 编程进阶智能体**


## 文档信息

- **版本**：v1.0
- **日期**：2026-06-14
- **适用对象**：有一定项目经验、熟悉 Git / Node.js / 终端操作、希望用编程智能体完成真实开发任务的开发者。

## 资料入口

- **内网课题页**：<http://172.28.21.141:3004/s/keti1/p/claude-hXgN3aOXQZ>
- 附件资料：add.txt
- **内部工具仓库**：<http://172.28.21.22:3000/xuedongzhang/claw-haha.git>

## 说明

- 本手册围绕“进阶篇”编程智能体使用场景编写，内容覆盖官方 Claude Code、内部 claw-haha 封装、gateway 模型适配、项目初始化、测试修复、跨文件重构、权限安全、成本控制与团队最佳实践。
- 内网课题页与内部 Git 地址需要在公司/实验室内网或 VPN 环境下访问；如当前机器无内网权限，请联系管理员或在内网终端中操作。
- 所有命令中的路径、API Key、模型名、仓库名都需要按你的实际环境替换。
- 不要把 .env、API Key、数据库密码、私有证书、云账号凭据提交到 Git，也不要把这些内容直接粘贴给智能体。


## 目录


- [01. 进阶篇定位](#01-进阶篇定位)
- [02. 核心概念：Claude Code、claw-haha 与 gateway](#02-核心概念claude-codeclaw-haha-与-gateway)
- [03. 安装前准备](#03-安装前准备)
- [04. 安装方式一：官方 Claude Code](#04-安装方式一官方-claude-code)
- [05. 安装方式二：内部 claw-haha](#05-安装方式二内部-claw-haha)
- [06. 登录、免登录与模型配置](#06-登录免登录与模型配置)
- [07. .env 与 ~/.claude/settings.json 的优先级](#07-env-与-claude-settingsjson-的优先级)
- [08. 常用命令速查](#08-常用命令速查)
- [09. 第一次进入项目：/init 与 CLAUDE.md](#09-第一次进入项目-init-与-claudemd)
- [10. 推荐的 CLAUDE.md 模板](#10-推荐的-claudemd-模板)
- [11. 常规运行模式](#11-常规运行模式)
- [12. 无交互模式与危险权限](#12-无交互模式与危险权限)
- [13. 典型开发工作流](#13-典型开发工作流)
- [14. 实战场景一：自动修复测试](#14-实战场景一自动修复测试)
- [15. 实战场景二：跨文件重构](#15-实战场景二跨文件重构)
- [16. 实战场景三：理解陌生项目](#16-实战场景三理解陌生项目)
- [17. 实战场景四：代码审查与安全审查](#17-实战场景四代码审查与安全审查)
- [18. Git、分支与提交规范](#18-git分支与提交规范)
- [19. Agents.md / 子智能体 / 多任务协作](#19-agentsmd-子智能体-多任务协作)
- [20. donkey/Agents.md 测试记录与优化建议](#20-donkey-agentsmd-测试记录与优化建议)
- [21. Token、耗时与成本控制](#21-token耗时与成本控制)
- [22. 国内用户与内部模型最佳实践](#22-国内用户与内部模型最佳实践)
- [23. 桌面版与 IDE 使用建议](#23-桌面版与-ide-使用建议)
- [24. 安全、权限与敏感文件保护](#24-安全权限与敏感文件保护)
- [25. 常见问题排查](#25-常见问题排查)
- [26. Prompt 模板库](#26-prompt-模板库)
- [27. 团队落地建议](#27-团队落地建议)
- [28. 快速检查清单](#28-快速检查清单)


<a id="01-进阶篇定位"></a>
## 01. 进阶篇定位


“进阶篇”的目标不是教用户把智能体当普通聊天工具使用，而是把它接入真实工程项目，让它能够：

1. 阅读项目结构和已有代码。
2. 根据明确目标制定修改计划。
3. 自动编辑多处文件。
4. 运行测试、lint、typecheck、build。
5. 根据报错继续定位并修复。
6. 输出变更总结、风险说明、测试结果。
7. 配合 Git 工作流完成提交、PR、代码审查。

适合人群：
- 已经能独立完成项目开发的工程师。
- 熟悉 Node.js、Python、Java、Go 等任意一种工程栈的开发者。
- 需要快速理解陌生项目、修复测试、做重构或迁移的开发者。
- 需要在本地模型、公司 gateway、官方 Claude Code 之间切换的内部用户。

不建议直接上手的人群：
- 完全不熟悉终端命令的新手。
- 没有 Git 基础、无法判断代码变更风险的用户。
- 在生产环境机器上直接运行智能体且没有任何权限隔离的用户。
- 想把密钥、凭据、客户数据直接交给模型分析的用户。

进阶篇的核心原则：
- 让智能体做“可验证的工程任务”，不要只让它做“泛泛的解释”。
- 每次任务都要求它给出计划、变更范围、测试命令和验证结果。
- 所有自动修改都要经过 git diff、测试、人工 review。
- 对危险命令、密钥文件、生产环境操作设置明确边界。


<a id="02-核心概念claude-codeclaw-haha-与-gateway"></a>
## 02. 核心概念：Claude Code、claw-haha 与 gateway


### 2.1 Claude Code 是什么

Claude Code 是面向开发者的编程智能体工具。它可以运行在终端、IDE、桌面应用或其他集成环境中。和普通聊天不同，它能够直接在项目目录里执行工程任务，例如：

- 搜索代码。
- 读取文件。
- 修改文件。
- 运行命令。
- 查看测试失败信息。
- 根据报错继续修复。
- 生成提交说明。
- 辅助创建 PR。
- 做本地代码审查。

可以把它理解为“在你的项目目录里工作的 AI 开发助手”。

### 2.2 claw-haha 是什么

claw-haha 是内部封装/适配层，通常用于把 Claude Code 风格的使用方式接入公司或团队自己的 gateway。它的作用可以概括为：

- 保留类似 Claude Code 的交互体验。
- 通过 gateway 适配不同后端模型。
- 在有 .env 时走内部/本地模型配置。
- 在没有 .env 时回退到标准 Claude Code 的 ~/.claude/settings.json 配置。
- 让用户尽量不用改业务代码，也不用频繁修改 LLM 接入逻辑。

### 2.3 gateway 的作用

你补充的结论里提到：“我们的 gateway 有一定的适配模型能力（不用改 LLM）”。在手册中可以理解为：

- 业务侧仍按 Claude Code / Anthropic 兼容接口调用。
- gateway 在中间处理模型名称、鉴权、协议转换、供应商差异。
- 切换模型时，优先修改 gateway 或 .env，而不是修改项目代码。
- 当 Qwen3.6-27B 等模型响应较慢时，可以在 gateway 层迁移到更快模型，例如计划替换为智谱 4.7，以获得更好的交互速度。

### 2.4 推荐使用路径

初学者：
- 优先使用桌面版或 IDE 插件。
- 只做读代码、解释项目、生成文档、简单修复。
- 不开启无交互危险权限。

有经验开发者：
- 使用终端模式。
- 先 /init。
- 明确任务目标和测试命令。
- 默认保留权限确认。
- 在隔离分支或临时目录中使用自动修复。

高级用户 / 自动化场景：
- 使用 claw-haha + gateway。
- 使用 .env 控制模型和 gateway API Key。
- 可在沙箱、CI、临时 worktree 中使用无交互模式。
- 严格限制 token、命令范围、GitHub Token 范围和扫描范围。


<a id="03-安装前准备"></a>
## 03. 安装前准备


### 3.1 环境要求

推荐环境：

- 操作系统：
  - macOS
  - Linux
  - Windows + WSL
  - Windows + Git Bash（可用，但复杂项目更推荐 WSL）

- 基础软件：
  - Node.js v18.0+
  - Git
  - npm
  - bun（内部 claw-haha 推荐）
  - 一个可用的终端：Terminal、iTerm2、Windows Terminal、VS Code Terminal 等

- 推荐硬件：
  - 内存 8GB+
  - 中大型项目建议 16GB+
  - 磁盘预留足够空间用于 node_modules、缓存、日志、测试产物

### 3.2 检查环境

在终端运行：

    node --version
    npm --version
    git --version

如果使用 bun：

    bun --version

如果没有 bun，可以先按内部安装方式执行：

    npm install -g bun

### 3.3 项目准备

进入业务项目之前，建议先确认 Git 状态：

    git status

建议工作方式：

    git checkout -b ai/your-task-name

例如：

    git checkout -b ai/fix-login-test
    git checkout -b ai/refactor-user-api
    git checkout -b ai/add-payment-docs

这样可以确保智能体修改都集中在独立分支中，便于回滚和 review。

### 3.4 安全准备

在项目根目录确认是否有敏感文件：

    .env
    .env.local
    .env.production
    secrets/
    credentials.json
    service-account.json
    id_rsa
    kubeconfig
    ~/.aws/credentials

建议在 .claude/settings.json 中禁止读取敏感文件，示例见后文“安全、权限与敏感文件保护”。


<a id="04-安装方式一官方-claude-code"></a>
## 04. 安装方式一：官方 Claude Code


### 4.1 推荐安装方式

官方较新的安装方式通常推荐使用原生安装器。macOS / Linux / WSL 可执行：

    curl -fsSL https://claude.ai/install.sh | bash

安装完成后验证：

    claude --version
    claude doctor

进入任意项目目录后启动：

    claude

### 4.2 npm 安装方式

如果你的团队环境仍使用 npm 方式，可以执行：

    npm install -g @anthropic-ai/claude-code

验证：

    claude --version

升级：

    npm install -g @anthropic-ai/claude-code@latest

**注意：**
- 不建议直接使用 sudo npm install -g，容易引起权限和安全问题。
- 如果 npm 全局目录无写权限，应配置用户级 npm global 目录，或使用 nvm 管理 Node.js。
- 如果内部旧文档中出现 sudo npm install -g，可作为历史方案理解；新环境优先用非 sudo 方案。

### 4.3 Windows 建议

Windows 用户优先使用 WSL：

    wsl --install

在 WSL 内安装 Node.js、Git、Claude Code 或 claw-haha。原因是很多开发工具链、权限模型、shell 行为在 Linux 环境中更稳定。


<a id="05-安装方式二内部-claw-haha"></a>
## 05. 安装方式二：内部 claw-haha


### 5.1 克隆内部仓库

在有内网权限的机器上执行：

    git clone http://172.28.21.22:3000/xuedongzhang/claw-haha.git
    cd claw-haha

### 5.2 安装 bun

如果本机没有 bun：

    npm install -g bun

验证：

    bun --version

### 5.3 安装依赖

在 claw-haha 目录执行：

    bun install

如果 bun 不可用，也可以尝试 npm：

    npm install

但内部推荐以仓库 README 或 env.example 说明为准。

### 5.4 配置 .env

复制示例环境文件：

    cp env.example .env

然后编辑 .env，把 gateway API Key、gateway 地址、模型名等改成你的真实配置。

示例写法仅供参考，字段名必须以 env.example 为准：

    GATEWAY_API_KEY=<your_gateway_api_key>
    ANTHROPIC_BASE_URL=<your_gateway_or_proxy_url>
    ANTHROPIC_MODEL=<model_name>

或者某些内部版本可能使用：

    API_KEY=<your_gateway_api_key>
    BASE_URL=<your_gateway_or_proxy_url>
    MODEL=<model_name>

**关键原则：**
- 字段名不要凭空猜，以 env.example 为准。
- .env 不要提交到 Git。
- .env 不要发到聊天窗口。
- 如果模型切换由 gateway 管理，本地只需要保留 gateway key 和统一入口即可。

### 5.5 在业务项目中运行

进入你的业务项目目录：

    cd <your-project-dir>

用完整路径启动：

    /path/to/claw-haha/bin/claude-haha

例如 claw-haha 在用户目录下：

    ~/claw-haha/bin/claude-haha

### 5.6 配置 alias

Linux / macOS 可添加 alias：

    alias claude-haha=~/claw-haha/bin/claude-haha

为了永久生效，写入 shell 配置文件：

zsh：

    echo 'alias claude-haha=~/claw-haha/bin/claude-haha' >> ~/.zshrc
    source ~/.zshrc

bash：

    echo 'alias claude-haha=~/claw-haha/bin/claude-haha' >> ~/.bashrc
    source ~/.bashrc

之后在任意项目目录直接运行：

    claude-haha

### 5.7 验证内部工具

在业务项目中运行：

    claude-haha

如果能正常进入交互界面，继续执行：

    /status
    /init

如果提示 command not found：
- 检查 alias 是否生效。
- 检查 bin/claude-haha 是否存在。
- 检查文件是否可执行：

    chmod +x ~/claw-haha/bin/claude-haha

如果提示鉴权失败：
- 检查 .env 是否存在。
- 检查 gateway API Key 是否正确。
- 检查当前网络是否能访问 gateway。
- 检查模型名是否被 gateway 支持。


<a id="06-登录免登录与模型配置"></a>
## 06. 登录、免登录与模型配置


### 6.1 官方登录

官方 Claude Code 通常可以直接运行：

    claude

首次运行会引导浏览器授权 Anthropic 账号。

也可以显式运行：

    claude auth login

查看登录状态：

    claude auth status --text

退出登录：

    claude auth logout

### 6.2 免登录配置思路

国内或内网环境中，官方登录可能不稳定，此时可以使用兼容 Anthropic API 的 gateway 或第三方模型服务。

附件资料里给出的免登录思路包括：

步骤 1：创建 ~/.claude.json，并写入：

    {
      "hasCompletedOnboarding": true
    }

步骤 2：创建 ~/.claude/settings.json，配置模型与环境变量。

示例一：DeepSeek 兼容入口

    {
      "env": {
        "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
        "ANTHROPIC_MODEL": "deepseek-chat",
        "ANTHROPIC_API_KEY": "<your_api_key>"
      }
    }

示例二：阿里云百炼兼容入口

    {
      "env": {
        "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max",
        "ANTHROPIC_API_KEY": "<your_api_key>"
      }
    }

**注意：**
- 上述字段是通用写法示例；如果使用内部 claw-haha，请优先以 env.example 为准。
- 不同兼容服务的 endpoint、模型名、鉴权字段可能不同。
- 不要把 API Key 写进项目级 .claude/settings.json 并提交到仓库。
- 个人 API Key 更适合放在用户级 ~/.claude/settings.json 或 shell 环境变量中。

### 6.3 内部 gateway 配置

使用 claw-haha 时，常见做法是：

    cp env.example .env
    vim .env

把 .env 改为内部 gateway 的 API Key 与模型配置。

你提供的关键规则：

1. gateway 有一定的适配模型能力，切换模型时通常不需要改 LLM 代码。
2. claw-code / claw-haha 如果使用 .env，则走本地/内部模型或 gateway 配置。
3. 如果没有 .env，则回到标准 Claude Code，读取 ~/.claude/settings.json。
4. 有桌面版本，对初学者更友好。
5. 当前 Qwen3.6-27B 偏慢，计划更换智谱 4.7，预期速度提升约 6 倍。

### 6.4 模型选择建议

按任务类型选择模型：

- 简单问答、读文件、写注释：
  - 使用轻量模型。
  - 目标是速度快、成本低。

- 日常开发、bug 修复、局部重构：
  - 使用中等能力模型。
  - 目标是稳定和性价比。

- 跨文件重构、复杂测试失败、架构分析：
  - 使用更强模型。
  - 目标是减少来回试错。

- 超长任务、自动跑测试、分析大仓库：
  - 使用强模型 + 明确范围 + 限制扫描路径。
  - 不建议无边界地让模型扫描整个组织或所有 GitHub 仓库。


<a id="07-env-与-claude-settingsjson-的优先级"></a>
## 07. .env 与 ~/.claude/settings.json 的优先级


### 7.1 内部规则

根据你补充的说明：

- claw-haha / claw-code 如果检测到 .env，会优先使用 .env 中的本地模型或 gateway 配置。
- 如果没有 .env，则按标准 Claude Code 方式使用 ~/.claude/settings.json。
- 团队 gateway 负责适配模型，用户通常不用修改 LLM 接入逻辑。

建议理解为：

    当前项目或工具目录 .env
        ↓ 优先
    内部 gateway / 本地模型配置
        ↓ 如果不存在 .env
    ~/.claude/settings.json
        ↓
    官方 Claude Code 配置 / 登录态

### 7.2 官方 Claude Code 的常见配置层级

Claude Code 通常存在多个配置层级：

- 用户级：
  - ~/.claude/settings.json
  - 只影响当前用户的所有项目。

- 项目级：
  - .claude/settings.json
  - 可提交到 Git，用于团队共享项目规则。

- 本地项目级：
  - .claude/settings.local.json
  - 只影响当前用户当前项目，不建议提交。

- 命令行参数：
  - 例如 claude --model xxx
  - 只影响本次启动。

- 会话内命令：
  - 例如 /model
  - 可在当前会话中切换模型。

### 7.3 推荐放置位置

个人 API Key：
- 放在用户级 ~/.claude/settings.json。
- 或放在 shell 环境变量。
- 不要提交。

团队共享规则：
- 放在项目 .claude/settings.json。
- 例如允许运行 npm test、禁止读取 .env。

业务项目说明：
- 放在 CLAUDE.md。
- 例如构建命令、测试命令、目录说明、编码规范。

本地临时配置：
- 放在 .claude/settings.local.json。
- 应加入 .gitignore。

内部 gateway 配置：
- claw-haha 使用 .env。
- 以 env.example 字段为准。
- 不提交。


<a id="08-常用命令速查"></a>
## 08. 常用命令速查


### 8.1 启动类

启动交互式会话：

    claude
    claude-haha

单次执行并退出：

    claude "帮我解释这个项目的启动流程"
    claude-haha "阅读 README 和 package.json，总结项目启动方式"

非交互 print 模式：

    claude -p "总结当前 git diff"

继续最近会话：

    claude --continue
    claude -c

恢复指定会话：

    claude --resume <session-id-or-name>

### 8.2 项目初始化

初始化项目说明：

    /init

这会生成或更新 CLAUDE.md，用来告诉智能体：
- 项目是什么。
- 如何安装依赖。
- 如何启动。
- 如何测试。
- 代码规范是什么。
- 哪些文件不能动。
- 常见任务怎么验证。

### 8.3 模型与状态

查看状态：

    /status

切换模型：

    /model

或：

    /model <model-name>

命令行指定模型：

    claude --model <model-name>

内部 claw-haha 模型通常通过 .env 或 gateway 管理。

### 8.4 上下文管理

清空当前任务上下文，开启新任务：

    /clear

压缩长对话，减少上下文占用：

    /compact

查看上下文占用：

    /context

**建议：**
- 一个任务完成后用 /clear 开新任务。
- 对话很长但任务还没结束时用 /compact。
- 不要在同一会话里连续塞入多个无关大任务。

### 8.5 成本与用量

查看用量：

    /usage

旧版本或部分封装中也可使用：

    /cost

**说明：**
- /cost 通常是 /usage 的别名。
- /usage 可查看 session cost、plan usage、活动统计等。
- 内部 gateway 的实际计费口径可能与官方不同，请以 gateway 日志或团队监控为准。

### 8.6 变更查看与回滚

查看 diff：

    /diff

回退到之前检查点：

    /rewind

旧命令别名：

    /undo

**建议：**
- 让智能体修改前先确认 git status。
- 修改后先看 /diff。
- 不满意时用 /rewind 或 git checkout 恢复。

### 8.7 代码审查

本地代码审查：

    /code-review

审查并尝试修复：

    /code-review --fix

安全审查：

    /security-review

普通 PR 审查：

    /review

### 8.8 诊断

诊断安装与配置：

    /doctor
    claude doctor

调试：

    /debug

帮助：

    /help


<a id="09-第一次进入项目-init-与-claudemd"></a>
## 09. 第一次进入项目：/init 与 CLAUDE.md


### 9.1 为什么必须先 /init

进阶用户最容易犯的错误是：直接让智能体改代码，但没有告诉它项目规范。

没有 CLAUDE.md 时，智能体需要临时猜测：
- 用 npm、pnpm、yarn 还是 bun？
- 测试命令是什么？
- 哪些目录是生成文件？
- API 层在哪里？
- 组件规范是什么？
- 提交格式是什么？
- 哪些文件不能修改？

执行 /init 后，智能体会生成 CLAUDE.md，作为后续任务的项目记忆。

### 9.2 初始化流程

进入项目根目录：

    cd <your-project-dir>

启动：

    claude-haha

执行：

    /init

或官方：

    claude
    /init

### 9.3 初始化后必须人工编辑

自动生成的 CLAUDE.md 只是起点，建议人工补齐：

- 项目简介。
- 关键目录。
- 安装命令。
- 启动命令。
- 测试命令。
- lint/typecheck/build 命令。
- 数据库迁移命令。
- 编码规范。
- 命名规范。
- Git 提交规范。
- 不允许修改的文件。
- 安全要求。
- 常见任务验证方式。

### 9.4 CLAUDE.md 的价值

好的 CLAUDE.md 可以明显提高：
- 代码修改命中率。
- 测试修复效率。
- 多文件重构一致性。
- 团队协作一致性。
- 新人上手速度。
- Token 利用效率。


<a id="10-推荐的-claudemd-模板"></a>
## 10. 推荐的 CLAUDE.md 模板


以下模板可复制到项目根目录 CLAUDE.md 中，再根据项目实际修改。

------------------------------------------------------------
# Project Guide

## 项目简介

这是一个 <项目类型> 项目，主要用于 <业务目标>。

## 技术栈

- Runtime: Node.js <version>
- Package Manager: <npm / pnpm / yarn / bun>
- Framework: <React / Vue / Next.js / Express / NestJS / ...>
- Test: <Jest / Vitest / Playwright / Pytest / ...>
- Lint: <ESLint / Biome / Ruff / ...>
- Typecheck: <tsc / mypy / ...>

## 常用命令

安装依赖：

    <install command>

启动开发环境：

    <dev command>

运行全部测试：

    <test command>

运行单个测试：

    <single test command>

Lint：

    <lint command>

Typecheck：

    <typecheck command>

Build：

    <build command>

## 目录说明

- src/：业务源码
- tests/：测试
- docs/：文档
- scripts/：脚本
- config/：配置
- generated/：生成文件，不要手动修改

## 编码规范

1. 优先修改最小范围。
2. 不要重写无关模块。
3. 不要改变公共 API，除非任务明确要求。
4. 新增逻辑必须补充或更新测试。
5. 修复 bug 时先复现，再修改，再验证。
6. 保持现有代码风格。
7. 不要引入新依赖，除非说明原因并经过确认。

## Git 规范

- 开始前先查看 git status。
- 修改后输出 git diff 摘要。
- 提交信息使用 Conventional Commits：
  - feat:
  - fix:
  - refactor:
  - test:
  - docs:
  - chore:

## 安全规则

禁止读取或输出以下文件内容：

- .env
- .env.*
- secrets/**
- credentials/**
- *.pem
- *.key
- service-account.json

不要把 token、密码、密钥写入代码或日志。

## 任务完成标准

每次修改后必须说明：

1. 修改了哪些文件。
2. 为什么这样改。
3. 运行了哪些验证命令。
4. 测试结果是什么。
5. 还有哪些风险或未覆盖点。
------------------------------------------------------------


<a id="11-常规运行模式"></a>
## 11. 常规运行模式


### 11.1 标准启动

在项目目录中：

    cp env.example .env
    claude-haha
    /init

**说明：**
- cp env.example .env 用于复制内部 gateway 或项目运行所需配置。
- 如果这是 claw-haha 的 .env，请填写 gateway API Key。
- 如果这是业务项目的 .env，请填写项目自身运行环境变量。
- 两类 .env 不要混淆，具体以仓库 README 和 env.example 为准。

### 11.2 推荐首个任务

第一次启动后，不要直接让它大改代码。建议先问：

    请阅读 README、package.json、src 目录结构，生成项目结构说明。
    不要修改任何文件，只输出：
    1. 项目用途
    2. 启动方式
    3. 测试方式
    4. 关键目录
    5. 可能的风险点

然后再让它执行 /init 或完善 CLAUDE.md。

### 11.3 日常任务模板

    我需要修复 <问题描述>。
    请先阅读相关文件并给出计划，不要立即修改。
    计划中请包含：
    1. 可能原因
    2. 需要查看的文件
    3. 修改范围
    4. 验证命令
    等我确认后再改。

如果你信任任务范围，也可以直接要求：

    修复 npm test 中失败的用例。
    要求：
    1. 先运行测试复现失败
    2. 定位原因
    3. 做最小修改
    4. 重新运行相关测试
    5. 输出 diff 摘要和风险说明


<a id="12-无交互模式与危险权限"></a>
## 12. 无交互模式与危险权限


### 12.1 命令

你提供的无交互模式：

    claude-haha --dangerously-skip-permissions
    /init

含义：
- 跳过权限确认。
- 智能体可能直接读取文件、修改文件、运行命令。
- 不会在每一步都询问你。
- 适合自动化测试、沙箱实验、一次性临时目录。
- 不适合生产仓库主分支、含密钥目录、重要数据目录。

### 12.2 风险

无交互模式可能导致：
- 自动修改大量文件。
- 自动运行耗时命令。
- 自动执行带副作用脚本。
- 自动访问网络。
- 自动读取不该读取的文件。
- 因测试命令不受限导致 token 和时间消耗增加。
- 使用 GITHUB_TOKEN 时扫描范围过大。

### 12.3 安全使用条件

只有满足以下条件时才建议使用：

1. 在独立分支或临时 worktree 中。
2. 已经 git status 确认没有未保存重要修改。
3. 已经配置敏感文件 deny 规则。
4. 项目测试命令明确且不会破坏环境。
5. API Key 权限最小化。
6. 不在生产服务器上运行。
7. 不使用高权限 GitHub Token 扫描全组织或全部 GitHub。
8. 可以随时通过 git reset --hard 或删除临时目录恢复。

### 12.4 更安全的替代方式

计划模式：

    claude --permission-mode plan

或在会话内要求：

    先给出计划，不要修改文件。

允许只读命令：

    --allowedTools "Read" "Bash(git diff *)" "Bash(git status *)"

项目级权限 allow/deny：

    .claude/settings.json

先让它只做分析，再人工确认修改，是团队协作中更稳妥的默认策略。


<a id="13-典型开发工作流"></a>
## 13. 典型开发工作流


### 13.1 推荐闭环

每个任务都按这个闭环执行：

    明确目标
      ↓
    查看项目规则
      ↓
    制定计划
      ↓
    最小范围修改
      ↓
    运行测试
      ↓
    查看 diff
      ↓
    代码审查
      ↓
    人工确认
      ↓
    提交 / PR

### 13.2 标准 Prompt

    任务：<一句话目标>

    背景：
    - 当前问题是：<问题>
    - 相关文件可能在：<路径>
    - 期望行为：<期望>
    - 当前行为：<当前>

    约束：
    - 只做最小必要修改
    - 不新增依赖，除非说明理由
    - 不修改 public API，除非必须
    - 不读取 .env 或 secrets
    - 修改后运行相关测试

    输出：
    1. 修改计划
    2. 修改文件列表
    3. 测试命令和结果
    4. 风险说明

### 13.3 要求智能体先计划

对于大任务，使用：

    先进入计划模式。
    请只输出执行计划和需要确认的问题，不要修改文件。

确认后：

    按计划执行，但每完成一个阶段先汇报 diff 摘要。

### 13.4 要求智能体持续验证

    修改后请运行：
    1. npm test -- <相关测试>
    2. npm run lint
    3. npm run typecheck

    如果失败，请继续修复，直到相关测试通过。
    如果失败原因与本任务无关，请停止并说明。


<a id="14-实战场景一自动修复测试"></a>
## 14. 实战场景一：自动修复测试


### 14.1 适用场景

- npm test 失败。
- CI 中某个测试失败。
- 单元测试断言不匹配。
- TypeScript 类型错误。
- lint 失败。
- 依赖升级后测试破坏。

### 14.2 推荐步骤

第一步：复现

    请先运行 npm test，记录失败用例和错误栈。
    不要修改文件。

第二步：定位

    根据失败栈定位相关源码和测试文件。
    输出可能原因，按可能性排序。

第三步：修改

    请做最小修改修复失败。
    不要修改测试期望，除非能证明测试期望错误。

第四步：验证

    请重新运行失败测试。
    如果通过，再运行相关测试套件。

第五步：总结

    请输出：
    1. 失败原因
    2. 修改文件
    3. 验证命令
    4. 测试结果
    5. 是否有未覆盖风险

### 14.3 一条命令式 Prompt

    npm test 当前失败。
    请按以下流程处理：
    1. 运行测试复现失败；
    2. 阅读失败栈和相关源码；
    3. 只做最小必要修改；
    4. 重新运行失败测试；
    5. 如果仍失败，继续迭代；
    6. 最后输出变更摘要、测试结果和风险。
    注意：不要读取 .env，不要改无关文件。

### 14.4 测试耗时控制

不要让智能体无脑运行全量测试。优先：

    npm test -- <test-name>
    npm test -- path/to/file.test.ts
    npm run test:unit -- <pattern>
    pnpm test path/to/file.test.ts
    pytest tests/test_x.py -q

全量测试只在最后阶段运行。


<a id="15-实战场景二跨文件重构"></a>
## 15. 实战场景二：跨文件重构


### 15.1 适用场景

- API 参数变更。
- 函数签名修改。
- 目录结构调整。
- 类型迁移。
- 老接口替换为新接口。
- 重复逻辑抽取。
- 组件拆分。

### 15.2 风险

跨文件重构的风险高于单点 bug 修复，原因是：
- 引用点多。
- 测试覆盖可能不足。
- 类型系统不一定能覆盖运行时行为。
- 自动修改可能遗漏动态调用。
- 文档、示例、mock、fixture 可能一起需要更新。

### 15.3 推荐 Prompt

    我要把 <old_api> 重构为 <new_api>。
    请先只做分析，不要修改。
    输出：
    1. 所有引用位置
    2. 调用方式分类
    3. 影响范围
    4. 推荐迁移步骤
    5. 需要运行的测试

确认后：

    按上面的迁移步骤执行。
    要求：
    - 分阶段修改；
    - 每阶段后运行 typecheck 或相关测试；
    - 不要改无关格式；
    - 输出最终 diff 摘要。

### 15.4 推荐验证命令

    npm run typecheck
    npm test -- <affected-pattern>
    npm run lint
    npm run build

如果是前端组件重构，还应考虑：
- Storybook 是否受影响。
- UI 快照是否变化。
- e2e 测试是否需要更新。


<a id="16-实战场景三理解陌生项目"></a>
## 16. 实战场景三：理解陌生项目


### 16.1 目标

让智能体帮助你快速得到：
- 项目用途。
- 技术栈。
- 启动流程。
- 请求链路。
- 数据模型。
- 核心模块。
- 测试方式。
- 风险点。

### 16.2 推荐 Prompt

    请理解这个陌生项目。
    不要修改任何文件。
    请阅读 README、package.json、配置文件和 src 目录，输出：
    1. 项目一句话介绍
    2. 技术栈
    3. 启动命令
    4. 测试命令
    5. 主要目录说明
    6. 一条典型请求从入口到业务逻辑的调用链
    7. 新人最应该先读的 5 个文件
    8. 潜在风险或 TODO

### 16.3 输出形式

要求智能体输出成文档：

    请把分析结果写入 docs/project-overview.md。
    但在写入前先展示目录结构和提纲，等我确认。

### 16.4 结合 /init

理解项目后，立即要求：

    请基于刚才的分析完善 CLAUDE.md。
    要包含构建、测试、目录、规范、安全限制。


<a id="17-实战场景四代码审查与安全审查"></a>
## 17. 实战场景四：代码审查与安全审查


### 17.1 本地变更审查

先查看变更：

    git diff

让智能体审查：

    请审查当前 git diff。
    重点关注：
    1. 正确性 bug
    2. 边界条件
    3. 类型错误
    4. 安全风险
    5. 是否有无关修改
    6. 是否需要测试

或使用命令：

    /code-review

### 17.2 自动修复审查意见

    /code-review --fix

**建议：**
- 小范围变更可以尝试 --fix。
- 大范围变更建议只输出意见，人工选择要不要改。
- 涉及安全、鉴权、支付、数据删除时不要自动修复后直接合并。

### 17.3 安全审查

    /security-review

重点检查：
- SQL 注入。
- 命令注入。
- SSRF。
- XSS。
- 鉴权绕过。
- 越权访问。
- token 泄露。
- 日志打印敏感信息。
- 文件路径穿越。
- 不安全反序列化。

### 17.4 审查 Prompt

    请对当前 diff 做安全审查。
    不要修改文件。
    输出：
    1. 高风险问题
    2. 中风险问题
    3. 低风险问题
    4. 每个问题对应文件和行号
    5. 建议修复方案
    6. 哪些地方需要人工确认


<a id="18-git分支与提交规范"></a>
## 18. Git、分支与提交规范


### 18.1 开始前

    git status
    git checkout -b ai/<task-name>

### 18.2 修改中

让智能体定期说明：

    请输出当前已修改文件列表和每个文件修改目的。

查看 diff：

    git diff

### 18.3 不满意时回滚

回滚单个文件：

    git checkout -- path/to/file

回滚全部未提交修改：

    git reset --hard

如果有新增文件：

    git clean -fd

**注意：**
- git reset --hard 和 git clean -fd 会删除未提交修改。
- 执行前必须确认没有重要手工改动。

### 18.4 提交前

    npm test
    npm run lint
    npm run typecheck
    git diff --check

让智能体生成提交信息：

    请根据当前 git diff 生成 Conventional Commit 信息。
    格式：
    <type>(<scope>): <summary>

    正文说明：
    - 修改内容
    - 测试结果
    - 风险

### 18.5 推荐提交类型

- feat: 新功能
- fix: bug 修复
- refactor: 重构
- test: 测试
- docs: 文档
- chore: 杂项
- perf: 性能优化
- build: 构建系统
- ci: CI 配置


<a id="19-agentsmd-子智能体-多任务协作"></a>
## 19. Agents.md / 子智能体 / 多任务协作


### 19.1 Agents.md 的作用

AGENTS.md 通常用于描述“给编码智能体看的项目规则”。它可以和 CLAUDE.md 配合使用：

- CLAUDE.md：更偏 Claude Code 会话记忆与项目操作指南。
- AGENTS.md：更偏通用编码智能体规则，可用于多种 agent 工具。

如果项目中已有 donkey/Agents.md 或类似文件，应让智能体先阅读：

    请先阅读 donkey/Agents.md 和 CLAUDE.md。
    总结里面对编码、测试、权限和交付的要求。
    不要修改文件。

### 19.2 子智能体适合做什么

适合拆分：
- 一个子任务做测试失败定位。
- 一个子任务做 API 引用搜索。
- 一个子任务做文档更新。
- 一个子任务做安全审查。
- 一个子任务做性能分析。

不适合拆分：
- 高耦合小改动。
- 需要统一上下文的业务逻辑。
- 涉及密钥或生产数据。
- 没有明确边界的大任务。

### 19.3 多任务协作原则

- 每个 agent 任务必须有明确输入和输出。
- 每个 agent 只负责一类工作。
- 最终由主会话合并结论。
- 不要让多个 agent 同时修改同一批文件。
- 大仓库任务必须限制路径范围。

### 19.4 推荐 Prompt

    请基于 donkey/Agents.md 拆分本任务。
    要求：
    1. 每个子任务都有清晰目标；
    2. 标明只读任务和可修改任务；
    3. 标明可能冲突的文件；
    4. 给出执行顺序；
    5. 先输出计划，不要执行。


<a id="20-donkey-agentsmd-测试记录与优化建议"></a>
## 20. donkey/Agents.md 测试记录与优化建议


### 20.1 现场测试记录

根据你提供的信息，testing plan donkey/Agents.md 的结果为：

- 总耗时约 14 分钟。
- 消耗约 11000 tokens。
- 实际编码时间约 5 分钟。
- 测试/扫描环节占主要时间。
- 原因之一是使用 GITHUB_TOKEN 扫描 GitHub 范围过大。

**说明：**
- 记录中“测试时间 around 15 min”和“总耗时 14 mins”可能来自不同统计口径或四舍五入。
- 对实际复盘来说，关键结论是：编码本身很快，耗时主要花在测试、扫描和外部 API/仓库访问上。

### 20.2 暴露的问题

1. GITHUB_TOKEN 权限可能过大。
2. 扫描范围没有限制到目标 repo。
3. 测试计划可能没有区分“必要测试”和“全量扫描”。
4. agent 在验证阶段消耗了大量时间与 token。
5. 如果模型较慢，等待时间会进一步放大。

### 20.3 优化建议

建议一：限制 GitHub Token 权限

- 使用 fine-grained token。
- 只授权目标 repository。
- 只授予必要权限，例如只读 contents、pull requests。
- 不要使用可访问所有组织仓库的高权限 token。

建议二：限制扫描范围

Prompt 中明确写：

    只扫描当前仓库，不要扫描我的全部 GitHub。
    如果需要访问 GitHub，只允许访问 <org>/<repo>。
    不要枚举无关仓库。

建议三：限制测试命令

    先运行与本任务相关的最小测试。
    不要运行全量 e2e，除非我确认。
    如果测试超过 5 分钟无输出，请停止并汇报。

建议四：分阶段验证

    阶段 1：静态检查
    阶段 2：相关单测
    阶段 3：局部集成测试
    阶段 4：人工确认后全量测试

建议五：记录 token 与耗时

每次任务结束要求输出：

    请输出本次任务的：
    1. 主要耗时阶段
    2. 运行过的命令
    3. 大概 token 消耗
    4. 下次可优化点

### 20.4 优化后的测试 Prompt

    请根据 donkey/Agents.md 执行测试计划，但必须遵守：
    1. 只读取当前仓库；
    2. 不扫描全部 GitHub；
    3. 如需 GitHub Token，只能访问当前 repo；
    4. 先运行最小相关测试；
    5. 每个命令超过 5 分钟无输出就停止；
    6. 不要开启全量 e2e，除非我确认；
    7. 最后汇报耗时、token 消耗、测试结果和风险。


<a id="21-token耗时与成本控制"></a>
## 21. Token、耗时与成本控制


### 21.1 为什么 token 会快速消耗

以下行为会显著增加 token：

- 让智能体阅读整个大仓库。
- 把大量日志直接贴进对话。
- 运行全量测试并反复粘贴失败输出。
- 长对话不 /compact。
- 多个无关任务放在同一会话。
- 大量工具输出进入上下文。
- 使用多个子智能体并行分析。
- 扫描 GitHub 全量仓库或大量 issue/PR。

### 21.2 控制策略

策略一：限定路径

    只分析 src/auth 和 tests/auth，不要扫描其他目录。

策略二：限定输出

    错误日志只保留前 100 行和最后 100 行。

策略三：限定测试

    先运行相关单测，不要运行全量测试。

策略四：压缩上下文

    /compact

策略五：新任务清空上下文

    /clear

策略六：查看用量

    /usage
    /cost

策略七：简单任务用轻量模型

    /model

策略八：关闭不必要的深度思考

内部模型或官方模型如支持 thinking / effort，可在简单任务中使用较低 effort。

### 21.3 推荐 Prompt

    请节省 token。
    只读取必要文件。
    不要输出大段源码。
    如果需要查看更多文件，先列出文件名和原因，等我确认。

### 21.4 长任务建议

大任务不要一次性说“帮我重构整个系统”。改成：

- 第一步：生成影响范围报告。
- 第二步：确认重构方案。
- 第三步：改接口定义。
- 第四步：改调用点。
- 第五步：改测试。
- 第六步：运行验证。
- 第七步：输出总结。

分阶段可以减少跑偏，也便于中途停止。


<a id="22-国内用户与内部模型最佳实践"></a>
## 22. 国内用户与内部模型最佳实践


### 22.1 常见问题

问题一：官方登录连不上

解决：
- 使用免登录配置。
- 使用内部 gateway。
- 使用兼容 Anthropic API 的第三方模型服务。
- 检查代理、证书、DNS、公司网络策略。

问题二：响应慢或卡顿

解决：
- /compact 压缩对话。
- /clear 开新会话。
- 换轻量模型。
- 限制读取范围。
- 不要让模型扫描大仓库。
- 检查 gateway 模型性能。
- 如果 Qwen3.6-27B 较慢，可按团队计划切换到更快模型，例如智谱 4.7。

问题三：Token 消耗快

解决：
- /usage 或 /cost 监控。
- 控制日志输出。
- 分阶段测试。
- 简单任务关闭深度思考。
- 不要在一个会话中做多个无关任务。

问题四：模型能力不稳定

解决：
- 在 CLAUDE.md 写清项目规则。
- 给出明确验收标准。
- 要求先计划再修改。
- 对关键任务使用更强模型。
- 对生成结果做人工 review。
- 让模型运行测试，不要只相信解释。

### 22.2 gateway 使用建议

- 模型切换优先在 gateway 配置或 .env 中完成。
- 业务项目不要硬编码模型名。
- 对不同模型保留统一 prompt 规范。
- 记录每种模型在任务中的表现：
  - 平均响应速度
  - 测试修复成功率
  - token 消耗
  - 是否容易跑偏
  - 对中文/英文代码注释的理解能力
  - 对长上下文的稳定性

### 22.3 模型性能升级记录

当前反馈：
- Qwen3.6-27B 太慢。
- 计划更换智谱 4.7。
- 预期速度提升约 6 倍。

建议升级后做 A/B 测试：

测试任务：
1. 小 bug 修复。
2. npm test 自动修复。
3. 跨文件 API 重构。
4. README/CLAUDE.md 文档生成。
5. donkey/Agents.md 测试计划执行。

记录指标：
- 首 token 时间。
- 总耗时。
- token 消耗。
- 修改正确率。
- 测试通过率。
- 人工返工次数。


<a id="23-桌面版与-ide-使用建议"></a>
## 23. 桌面版与 IDE 使用建议


### 23.1 桌面版适合谁

你补充的信息中提到“有桌面版本，对于初学者友好”。建议定位如下：

适合：
- 不熟悉终端的新用户。
- 需要图形化查看 diff 的用户。
- 需要同时管理多个任务的用户。
- 需要更直观地查看会话、变更和状态的用户。

不适合：
- 高度自动化脚本。
- CI 集成。
- 复杂 shell 工作流。
- 需要精细控制环境变量和权限的高级场景。

### 23.2 VS Code / Cursor

适合：
- 在编辑器内选中代码后提问。
- 查看 inline diff。
- 结合终端运行测试。
- 对初学者更友好。

**注意：**
- IDE 插件和 CLI 可能使用同一套 ~/.claude/settings.json。
- IDE 中打开的文件和选中的代码可能成为上下文。
- 不要在 IDE 中打开 .env 后直接让模型读取当前选择。
- 对敏感文件配置 deny 规则。

### 23.3 终端模式

适合：
- 高级开发者。
- 自动修复测试。
- 跨文件重构。
- Git 工作流。
- CI / 脚本化任务。
- 内部 claw-haha / gateway 使用。

**建议：**
- 默认使用终端模式学习核心能力。
- 新用户可从桌面版过渡到终端。
- 团队培训时可先演示桌面版，再演示 CLI。


<a id="24-安全权限与敏感文件保护"></a>
## 24. 安全、权限与敏感文件保护


### 24.1 必须保护的文件

建议永远不要让智能体读取：

- .env
- .env.local
- .env.production
- .env.*
- secrets/**
- credentials/**
- service-account.json
- *.pem
- *.key
- id_rsa
- kubeconfig
- ~/.aws/credentials
- ~/.ssh/**
- 数据库 dump
- 客户隐私数据
- 生产日志原文

### 24.2 .claude/settings.json deny 示例

在项目根目录创建：

    mkdir -p .claude
    vim .claude/settings.json

写入：

    {
      "permissions": {
        "deny": [
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)",
          "Read(./credentials/**)",
          "Read(./config/credentials.json)",
          "Read(./service-account.json)",
          "Read(./*.pem)",
          "Read(./*.key)",
          "Bash(curl *)",
          "Bash(wget *)",
          "Bash(rm -rf *)"
        ],
        "ask": [
          "Bash(git push *)",
          "Bash(npm publish *)",
          "Bash(docker push *)",
          "Bash(kubectl *)",
          "Bash(terraform apply *)"
        ],
        "allow": [
          "Bash(git status)",
          "Bash(git diff *)",
          "Bash(npm test *)",
          "Bash(npm run lint *)",
          "Bash(npm run typecheck *)"
        ]
      }
    }

### 24.3 .gitignore 检查

确保：

    .env
    .env.*
    .claude/settings.local.json
    secrets/
    credentials/
    *.pem
    *.key

都在 .gitignore 中。

### 24.4 GITHUB_TOKEN 安全

如果任务需要 GitHub：

- 使用 fine-grained token。
- 只授权当前仓库。
- 不要给 admin 权限。
- 不要让智能体打印 token。
- 不要让智能体读取保存 token 的 .env。
- 使用命令时通过环境变量传递，而不是写入文件。
- 明确限制访问范围：

    只允许访问当前仓库，不要列出或扫描我的全部 GitHub 仓库。

### 24.5 生产环境禁区

除非有明确审批，不要让智能体执行：

    kubectl apply
    terraform apply
    npm publish
    docker push
    rm -rf
    psql production
    mysql production
    aws iam *
    aws s3 rm
    gh repo delete

如果确实需要生产操作：
- 使用只读模式先分析。
- 让智能体生成命令草案。
- 人工审查。
- 人工执行。
- 不要让无交互模式直接执行。


<a id="25-常见问题排查"></a>
## 25. 常见问题排查


### 25.1 claude-haha: command not found

检查 alias：

    alias claude-haha

检查路径：

    ls -l ~/claw-haha/bin/claude-haha

设置可执行：

    chmod +x ~/claw-haha/bin/claude-haha

重新加载 shell：

    source ~/.zshrc
    source ~/.bashrc

### 25.2 bun install 失败

尝试：

    bun --version
    npm install -g bun
    bun install --verbose

如果仍失败：

    npm install

检查 Node 版本：

    node --version

### 25.3 .env 不生效

检查：
- .env 是否在工具期望的位置。
- 字段名是否与 env.example 一致。
- API Key 是否有多余空格。
- base url 是否包含路径。
- 模型名是否被 gateway 支持。
- 是否启动的是正确的 claude-haha。

可以临时输出非敏感配置：

    grep -v KEY .env
    grep -v TOKEN .env

不要打印完整 API Key。

### 25.4 官方模式和内部模式混淆

现象：
- 明明配置了 .env，但仍走官方登录。
- 删除 .env 后模型变了。
- ~/.claude/settings.json 与 .env 配置冲突。

处理：
- 确认当前启动命令是 claude 还是 claude-haha。
- 确认当前目录是否有 .env。
- 确认 claw-haha 是否从自身目录或业务目录读取 .env。
- 没有 .env 时，按标准 Claude Code 配置读取 ~/.claude/settings.json。

### 25.5 模型很慢

处理：
- /compact
- /clear
- 换轻量模型
- 限制路径
- 减少日志
- 不要扫描大仓库
- 不要让它读 node_modules、dist、build
- 检查 gateway 当前模型
- 对 Qwen3.6-27B 等慢模型，按团队计划切到更快模型

### 25.6 修改太多文件

处理：
- 停止当前任务。
- 查看 git diff --stat。
- 让智能体解释每个文件为什么被改。
- 不合理则 /rewind 或 git reset。
- 下次 prompt 中明确“只允许修改以下文件”。

### 25.7 测试跑太久

处理：
- Ctrl+C 停止。
- 要求只运行相关测试。
- 给命令设置超时。
- 不要无交互跑全量 e2e。
- 检查是否扫描了外部 GitHub 或网络资源。

### 25.8 Token 消耗异常

处理：
- /usage 或 /cost。
- /compact。
- /clear。
- 让智能体不要输出大段源码。
- 不要贴完整日志。
- 限制 GitHub / 文件扫描范围。

### 25.9 权限提示太多

处理：
- 对常用只读命令加 allow。
- 对危险命令加 ask 或 deny。
- 不要直接用 dangerously-skip-permissions 解决所有提示。
- 对可信测试命令可加 allow，例如 npm test、npm run lint。


<a id="26-prompt-模板库"></a>
## 26. Prompt 模板库


### 26.1 项目理解

    请理解当前项目。
    不要修改文件。
    阅读 README、package.json、配置文件和 src 目录，输出：
    1. 项目用途
    2. 技术栈
    3. 启动命令
    4. 测试命令
    5. 核心目录
    6. 关键调用链
    7. 新人阅读顺序
    8. 风险点

### 26.2 生成 CLAUDE.md

    请根据当前项目生成 CLAUDE.md。
    要包含：
    - 项目简介
    - 技术栈
    - 安装命令
    - 启动命令
    - 测试命令
    - lint/typecheck/build
    - 目录说明
    - 编码规范
    - Git 规范
    - 安全限制
    生成前先输出提纲，等我确认。

### 26.3 修复测试

    npm test 失败。
    请先运行测试复现。
    然后定位失败原因，做最小修改。
    修改后重新运行相关测试。
    不要修改无关文件。
    最后输出修改摘要、测试结果和风险。

### 26.4 修复 TypeScript 错误

    npm run typecheck 失败。
    请运行命令并修复类型错误。
    要求：
    - 不使用 any 绕过，除非解释原因；
    - 不改变公共 API，除非必须；
    - 修改后重新运行 typecheck。

### 26.5 跨文件重构

    我要把 <旧接口> 替换为 <新接口>。
    先不要修改。
    请找出所有引用点，按调用类型分类，给出迁移计划。
    计划确认后再分阶段修改并运行测试。

### 26.6 代码审查

    请审查当前 git diff。
    不要修改文件。
    重点关注：
    - 正确性
    - 边界条件
    - 安全风险
    - 是否有无关修改
    - 是否缺测试
    输出按高/中/低风险排序。

### 26.7 生成提交信息

    请根据当前 git diff 生成提交信息。
    使用 Conventional Commits。
    同时输出：
    1. 变更摘要
    2. 测试结果
    3. 风险说明

### 26.8 文档更新

    请根据当前实现更新 README。
    要求：
    - 不夸大功能
    - 命令必须与 package.json 一致
    - 补充常见问题
    - 不泄露内部 API Key 或私有地址

### 26.9 限制范围

    本任务只允许分析和修改：
    - src/auth/**
    - tests/auth/**
    不要读取或修改其他目录。
    如果你认为必须修改其他文件，请先说明原因并等待确认。

### 26.10 限制 GitHub 扫描

    如果需要使用 GITHUB_TOKEN，请只访问当前仓库。
    不要列出、扫描或读取我的全部 GitHub 仓库。
    不要访问无关组织、issue 或 PR。


<a id="27-团队落地建议"></a>
## 27. 团队落地建议


### 27.1 统一项目模板

每个项目建议包含：

    CLAUDE.md
    AGENTS.md
    .claude/settings.json
    docs/ai-workflow.md

### 27.2 统一安全规则

团队应统一禁止：
- 读取 .env。
- 输出 token。
- 访问生产环境。
- 自动执行破坏性命令。
- 用高权限 GitHub Token 做无边界扫描。

### 27.3 统一任务流程

每个 AI 任务必须留下：
- 任务描述。
- 修改文件。
- 测试命令。
- 测试结果。
- 风险说明。
- 人工 reviewer。

### 27.4 建议培训路径

第一阶段：只读
- 项目理解。
- 代码解释。
- 文档生成。

第二阶段：小修改
- 修复 lint。
- 修复单测。
- 改注释、改文档。

第三阶段：中等任务
- 局部 bug 修复。
- 新增小功能。
- 添加测试。

第四阶段：高级任务
- 跨文件重构。
- 自动化测试修复。
- 安全审查。
- 子智能体并行分析。

### 27.5 指标体系

建议记录：
- 每次任务耗时。
- token 消耗。
- 测试通过率。
- 人工修改次数。
- 回滚次数。
- 高风险问题数。
- 模型响应速度。
- 不同模型的成功率。

### 27.6 模型替换评估

从 Qwen3.6-27B 切换到智谱 4.7 后，建议用同一组任务对比：

- 任务 A：读项目并生成 CLAUDE.md。
- 任务 B：修复一个失败单测。
- 任务 C：执行 donkey/Agents.md 测试计划。
- 任务 D：跨文件接口重构。
- 任务 E：安全审查当前 diff。

对比：
- 总耗时。
- 首响应时间。
- token 消耗。
- 是否一次成功。
- 是否出现无关修改。
- 测试是否通过。
- 人工 review 负担。


<a id="28-快速检查清单"></a>
## 28. 快速检查清单


### 28.1 安装检查

    node --version
    npm --version
    git --version
    bun --version
    claude --version
    claude doctor

claw-haha：

    ls -l ~/claw-haha/bin/claude-haha
    claude-haha

### 28.2 配置检查

    test -f .env && echo ".env exists"
    test -f ~/.claude/settings.json && echo "settings exists"
    git status

检查 .env 是否被忽略：

    git check-ignore .env

### 28.3 项目初始化检查

    test -f CLAUDE.md && echo "CLAUDE.md exists"
    test -f AGENTS.md && echo "AGENTS.md exists"

如果没有：

    /init

### 28.4 安全检查

确认 .claude/settings.json 中包含：

    Read(./.env)
    Read(./.env.*)
    Read(./secrets/**)

确认危险命令没有自动 allow：

    rm -rf
    git push
    npm publish
    kubectl
    terraform apply

### 28.5 任务前检查

- 是否在独立分支？
- 是否 git status 干净？
- 是否明确任务目标？
- 是否明确修改范围？
- 是否明确测试命令？
- 是否禁止读取敏感文件？
- 是否需要限制 GitHub Token 范围？

### 28.6 任务后检查

- 是否查看 git diff？
- 是否运行相关测试？
- 是否运行 lint/typecheck？
- 是否让智能体输出风险说明？
- 是否人工 review？
- 是否确认没有密钥泄露？
- 是否生成合理 commit message？


## 附录 A：推荐 .claude/settings.json


可作为项目级基础模板：

    {
      "$schema": "https://json.schemastore.org/claude-code-settings.json",
      "permissions": {
        "allow": [
          "Bash(git status)",
          "Bash(git diff *)",
          "Bash(git log *)",
          "Bash(npm test *)",
          "Bash(npm run test *)",
          "Bash(npm run lint *)",
          "Bash(npm run typecheck *)",
          "Bash(pnpm test *)",
          "Bash(pnpm run lint *)",
          "Bash(pnpm run typecheck *)",
          "Bash(bun test *)"
        ],
        "ask": [
          "Bash(git push *)",
          "Bash(npm publish *)",
          "Bash(docker push *)",
          "Bash(kubectl *)",
          "Bash(terraform apply *)",
          "Bash(gh pr merge *)"
        ],
        "deny": [
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)",
          "Read(./credentials/**)",
          "Read(./service-account.json)",
          "Read(./*.pem)",
          "Read(./*.key)",
          "Bash(rm -rf *)",
          "Bash(curl *|sh)",
          "Bash(wget *|sh)"
        ]
      }
    }


## 附录 B：推荐 .env 管理规则


内部 claw-haha 示例流程：

    git clone http://172.28.21.22:3000/xuedongzhang/claw-haha.git
    cd claw-haha
    npm install -g bun
    bun install
    cp env.example .env
    vim .env

业务项目运行：

    cd <your-project-dir>
    ~/claw-haha/bin/claude-haha

或配置 alias：

    alias claude-haha=~/claw-haha/bin/claude-haha

常规运行：

    cp env.example .env
    claude-haha
    /init

**注意：**
- 如果 .env 是内部 gateway 配置，请不要与业务项目运行配置混淆。
- 如果 .env 在当前目录不生效，请查看 claw-haha README 或启动脚本确认读取路径。
- 如果删除 .env，claw-haha 可能回退到标准 Claude Code 的 ~/.claude/settings.json。


## 附录 C：无交互模式操作建议


命令：

    claude-haha --dangerously-skip-permissions
    /init

只建议用于：
- 临时目录。
- 测试仓库。
- 沙箱。
- CI 自动化。
- 已限制权限的 worktree。

不建议用于：
- 主分支。
- 生产服务器。
- 有密钥的目录。
- 未提交手工修改的工作区。
- 高权限 GitHub Token 环境。

更稳妥的 Prompt：

    你现在可以自动执行任务，但必须遵守：
    1. 不读取 .env 或 secrets；
    2. 不执行 git push；
    3. 不执行 rm -rf；
    4. 不扫描全部 GitHub；
    5. 每次运行测试前说明命令；
    6. 只修改与任务相关的文件；
    7. 完成后输出 diff 摘要和测试结果。


## 附录 D：一分钟上手版


1. 安装内部工具：

    git clone http://172.28.21.22:3000/xuedongzhang/claw-haha.git
    cd claw-haha
    npm install -g bun
    bun install
    cp env.example .env
    vim .env

2. 配置 alias：

    echo 'alias claude-haha=~/claw-haha/bin/claude-haha' >> ~/.zshrc
    source ~/.zshrc

3. 进入项目：

    cd <your-project-dir>
    git checkout -b ai/init-claude-guide

4. 启动：

    claude-haha

5. 初始化：

    /init

6. 第一个安全任务：

    请阅读项目结构，不要修改文件。
    输出项目简介、启动命令、测试命令和核心目录。

7. 第一个修复任务：

    请运行相关测试，修复失败用例。
    做最小修改，最后输出测试结果和 diff 摘要。


## 附录 E：本手册维护建议


建议团队后续持续补充：

- 内部 gateway 最新地址。
- 当前推荐模型。
- 智谱 4.7 替换后的实测速度。
- claw-haha env.example 字段说明。
- 常见报错截图或日志。
- 不同项目的 CLAUDE.md 示例。
- donkey/Agents.md 的最终最佳实践版本。
- 团队统一权限模板。
- 成本统计和模型对比表。

手册更新原则：
- 命令必须可复制执行。
- 涉及密钥的地方只写占位符。
- 内部地址只写入口，不写敏感参数。
- 每条最佳实践最好有实际案例支撑。
- 新模型上线后必须更新“模型选择建议”和“性能记录”。
