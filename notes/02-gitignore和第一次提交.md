# .gitignore 和第一次提交

## 什么是 .gitignore？

`.gitignore` 是 Git 的"忽略清单"。你写在里面的文件/文件夹，Git 会自动忽略它们——`add` 的时候不会加进去，`status` 的时候也不会显示。

**为什么需要它？**

| 文件/文件夹 | 为什么忽略 |
|------------|-----------|
| `venv/` | 虚拟环境每个人自己生成，不能上传 |
| `.idea/` | PyCharm 个人配置，和别人无关 |
| `__pycache__/` | Python 自动生成的缓存文件 |
| `*.pyc` | 编译过的 Python 文件 |
| `.env` | 可能包含 API Key、密码等敏感信息 |

**核心原则：** 只上传"代码本身"，不上传"开发环境"。

---

## 三个工作区 — 详细理解

```
工作区（Working Directory）    暂存区（Staging Area）    本地仓库（Repository）
      ↓                              ↓
  你看到的文件                 git add 后的文件         git commit 后的文件
  (.gitignore 没写)                                          ↓
                                                         永久存档
```

**口诀：** `add` 放暂存 → `commit` 拍照片

---

## 实操记录

### git status — 随时查看当前状态

```bash
git status
```

会告诉你：
- 哪些文件被改动了（红色）
- 哪些文件在暂存区（绿色）
- 当前在哪个分支上

### git add — 把文件放进暂存区

```bash
git add .gitignore        # 添加单个文件
git add notes/            # 添加整个文件夹
git add .                 # 添加所有改动（慎用，容易加进不该加的文件）
```

### git commit — 拍照存档

```bash
git commit -m "提交说明"
```

**提交说明的规范：**
- 用中文或英文都行
- 简洁明了，概括本次改动
- 常用动词：add（添加）、fix（修复）、update（更新）、refactor（重构）

---

## 第一次提交的流程（标准模板）

```bash
# 1. 看看当前状态
git status

# 2. 添加文件到暂存区
git add .gitignore
git add notes/

# 3. 再次确认要提交的内容
git status

# 4. 拍照存档
git commit -m "初始化项目：添加 .gitignore 和笔记"
```
