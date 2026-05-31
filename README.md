# PR Craft

> AI 自动化 PR 系统 — 输入需求，AI 自动完成代码编写、审查并提交 Pull Request。

## 项目介绍

PR Craft 是一个基于 LangGraph 多 Agent 编排的自动化 PR 系统。当你提交一个需求（Issue），系统会自动完成：

1. **规划方案** — 架构师 Agent 分析需求，制定实现方案
2. **编写代码** — 程序员 Agent 根据方案生成代码
3. **审查代码** — 审查员 Agent 检查代码质量
4. **创建 PR** — 审查通过后自动创建 GitHub Pull Request

## 技术栈

| 层次 | 技术 | 版本 |
|------|------|------|
| **AI 编排** | LangGraph | 1.2.2 |
| **AI 模型** | DeepSeek API（兼容 OpenAI 格式） | — |
| **后端框架** | FastAPI + Uvicorn | 0.136.3 / 0.48.0 |
| **数据库** | PostgreSQL（Neon 云数据库）+ SQLAlchemy | 2.0.50 |
| **前端** | React + Vite + Ant Design | 19.2.6 / 8.0.12 / 6.4.3 |
| **GitHub 集成** | PyGithub | 2.9.1 |
| **代码质量** | ruff + pre-commit | — |
| **日志** | loguru | — |

## 运行环境

| 工具 | 版本 |
|------|------|
| Python | 3.12.13（conda 环境：pr-craft） |
| Node.js | 24.16.0 |
| npm | 11.13.0 |
| pip | 24.3.1 |

## 架构图

```
用户输入需求
      │
      ▼
┌─────────────────────────────────────┐
│       FastAPI 后端 API 接口          │
│  POST /api/tasks → 创建任务         │
│  GET  /api/tasks  → 任务列表        │
│  GET  /api/tasks/{id} → 任务详情    │
│  DELETE /api/tasks/{id} → 删除任务  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     LangGraph 多 Agent 工作流       │
│                                     │
│  Planner → Coder → Reviewer ──→ 通过│
│  架构师    程序员    审查员     │    │
│               ↑              │ 不通过│
│               └──── 重试 ≤3 ─┘      │
└──────────────┬──────────────────────┘
               │ 通过
               ▼
┌─────────────────────────────────────┐
│   GitHub API                        │
│   创建分支 → 提交代码 → 创建 PR     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   React 前端看板                     │
│   创建任务 · 状态跟踪 · 查看代码     │
└─────────────────────────────────────┘
```

## 快速开始

### 前置要求

- Python 3.12+
- Node.js 24+
- PostgreSQL 数据库（本机或 Neon 云数据库）
- DeepSeek API Key
- GitHub Personal Access Token（需 repo 权限）

### 1. 克隆项目

```bash
git clone https://github.com/dxr-coder/pr-craft.git
cd pr-craft
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
API_KEY=你的_deepseek_api_key
GITHUB_TOKEN=你的_github_token
DATABASE_URL=你的_postgresql_连接地址
```

### 3. 启动后端

推荐使用 conda 环境：

```bash
# 创建并激活 conda 环境
conda create -n pr-craft python=3.12
conda activate pr-craft

# 安装依赖
pip install -r requirements.txt

# 启动
uvicorn app.main:app --reload
```

或者使用 venv：

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 5. 访问

- 后端 API：http://localhost:8000
- API 文档（Swagger）：http://localhost:8000/docs
- 前端页面：http://localhost:5173

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/tasks/` | 获取任务列表（按创建时间正序） |
| POST | `/api/tasks/?issue=...` | 创建新任务（自动触发 AI 工作流，后台运行） |
| GET | `/api/tasks/{id}` | 获取任务详情 |
| DELETE | `/api/tasks/{id}` | 删除任务 |

## 项目结构

```
pr-craft/
├── app/                        # Python 后端
│   ├── main.py                 # FastAPI 入口
│   ├── agents/
│   │   ├── planner.py          # 架构师 Agent
│   │   ├── coder.py            # 程序员 Agent
│   │   ├── reviewer.py         # 审查员 Agent
│   │   └── orchestrator.py     # LangGraph 编排
│   ├── core/
│   │   ├── config.py           # 配置管理
│   │   ├── llm.py              # LLM 调用（DeepSeek）
│   │   ├── logger.py           # 结构化日志
│   │   ├── exceptions.py       # 统一异常处理
│   │   └── middleware.py       # CORS 中间件
│   ├── database/
│   │   ├── connection.py       # 数据库连接
│   │   ├── models.py           # 数据表模型
│   │   └── depends.py          # 依赖注入
│   ├── github/
│   │   ├── client.py           # GitHub 客户端
│   │   └── pr_manager.py       # PR 管理
│   └── routers/
│       ├── health.py           # 健康检查
│       └── tasks.py            # 任务 CRUD + 工作流
├── frontend/                   # React 前端
│   └── src/
│       ├── App.jsx             # 主页面
│       ├── App.css             # 样式
│       └── main.jsx            # 入口
├── notes/                      # 学习笔记（本地，不上传）
├── .env                        # 环境变量（不上传）
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── requirements.txt
```

## 特性

- **多 Agent 协作**：架构师、程序员、审查员三个 AI Agent 协同工作
- **自动重试**：审查不通过自动返工，最多重试 3 次
- **异步处理**：API 即时响应，AI 工作流在后台运行
- **代码规范**：ruff 自动检查 + pre-commit 提交前拦截
- **统一异常处理**：所有 API 错误返回统一 JSON 格式
- **结构化日志**：loguru 替代 print，带时间戳和文件位置
- **实时轮询**：前端自动刷新处理中的任务状态
