# sports-data-dashboard 🚴‍♂️📊

**运动数据仪表盘** - 基于 Vue3 + TypeScript 的运动数据可视化展示平台

[![Vue.js](https://img.shields.io/badge/Vue.js-3.5+-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-6.0+-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-8.0+-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![ECharts](https://img.shields.io/badge/ECharts-5.6+-AA344D?style=flat-square&logo=apache-echarts)](https://echarts.apache.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.2+-06B6D4?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## ✨ 项目简介

本项目是一个功能完整的**运动数据可视化仪表盘**，用于展示和管理运动数据（支持骑行、跑步、游泳等多种运动类型）。系统采用前后端分离架构：

- **前端**：Vue3 + TypeScript + Vite 构建的现代化单页应用（SPA）
- **后端**：Python CLI 工具，负责 FIT 文件解析、数据库管理和数据导出
- **数据存储**：SQLite 数据库（后端）+ JSON 文件（前端读取）

### 🎯 核心特性

#### 数据管理（Python CLI）
- ✅ **FIT 文件解析**：支持 Garmin 等设备的 .fit 文件，提取 16 个运动数据字段
- ✅ **数据库管理**：SQLite 存储，支持 CRUD 操作，自动去重
- ✅ **JSON 导出**：将数据库数据导出为 JSON 格式供前端使用
- ✅ **用户管理**：支持用户信息的初始化、查看、更新和删除
- ✅ **批量操作**：支持批量导入 FIT 文件、按日期范围删除记录

#### 数据可视化（Vue3 前端）
- 📅 **日历热力图**：年度运动数据概览，类似 GitHub 贡献图
  - 7 级颜色强度映射
  - 5 种着色指标切换（距离/时长/次数/热量/平均速度）
  - 年份选择器（弹窗式，3 列网格布局）
  - 今天标记（红色边框高亮）
- 📊 **柱形图统计**：多维度数据分析
  - 4 种显示模式（周/月/年/全部）
  - 5 种纵轴指标切换
  - 动态横轴配置（天/月/年）
  - 内置翻页组件
- 📋 **运动列表**：详细运动记录表格
  - 11 列数据字段展示
  - 分页、排序、筛选功能
  - 中文类型映射和单位格式化
- 👤 **个人信息面板**
  - 用户头像、名称、简介展示
  - 最近 1 周运动统计（5 项指标）

#### 技术亮点
- 🎨 **现代化 UI**：Tailwind CSS 4.2+，响应式设计，渐变色彩方案
- ⚡ **高性能**：组件懒加载、ECharts 实例复用、Pinia 状态缓存
- 🔒 **类型安全**：完整的 TypeScript 类型定义（interfaces, types）
- 📱 **响应式布局**：支持桌面端、平板、移动端（断点适配）
- 🎭 **丰富交互**：Hover 效果、过渡动画、Tooltip 提示

---

## 📸 功能预览

### 仪表盘页面（Dashboard）
```
┌──────────────────────────────────────────────────┐
│  👤 神骏 · 练习骑行中    [仪表盘] [运动记录] [地图] │
├──────────────┬───────────────────────────────────┤
│ 📊 本周统计   │  📅 日历热力图 (2026)             │
│              │  [距离][时长][次数][热量][速度]      │
│ 🚴 127.5 km  │  ┌─────────────────────────────┐  │
│ ⏱️ 8:32:15   │  │  ████ ░░ ███ ░░░ ██ ░░ ████ │  │
│ #️⃣ 12 次     │  │  ██ ░░░ ████ ░░ ██ ░░░ ███  │  │
│ 🔥 2,450 kcal│  │  ░░ ████ ░░░ ███ ██ ░░░ ████│  │
│ ⚡ 23.5 km/h │  │  (53周 × 7天 网格)           │  │
│              │  └─────────────────────────────┘  │
│ 04/01 - 04/07│  [◀ 2026 ▶]  图例: ···│▪ 今天   │
├──────────────┴───────────────────────────────────┤
│  📈 柱形图统计视图                                │
│  [周] [月] [年] [全部]  统计: 127.5km | 8h32m | ...│
│  ┌────────────────────────────────────────────┐ │
│  │  ██  ███  █  █████  ████  █  ██████  ███  │ │
│  │  (渐变色柱状图，支持指标切换)                 │ │
│  └────────────────────────────────────────────┘ │
│                    [◀ 04/01 - 04/07 ▶]            │
└──────────────────────────────────────────────────┘
```

### 运动记录页面（Activities）
```
┌──────────────────────────────────────────────────┐
│  👤 神骏 · 练习骑行中    [仪表盘] [运动记录] [地图] │
├──────────────────────────────────────────────────┤
│  运动列表                                        │
│  类型: [全部 ▼]                                   │
│  ┌────────────────────────────────────────────┐ │
│  │ 日期       │类型│距离(km)│时长    │...      │ │
│  ├────────────────────────────────────────────┤ │
│  │2026-03-26  │骑行│  8.11 │0:28:17 │...      │ │
│  │2026-03-24  │骑行│ 45.20 │1:42:30 │...      │ │
│  │2026-03-22  │跑步│ 10.05 │0:55:00 │...      │ │
│  │    ...     │... │  ...  │  ...   │...      │ │
│  └────────────────────────────────────────────┘ │
│  显示 1-10 条，共 558 条    [< 1 2 3 ... 56 >]   │
└──────────────────────────────────────────────────┘
```

---

## 🛠️ 技术栈

### 前端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue.js** | 3.5+ | 渐进式 JavaScript 框架（Composition API） |
| **TypeScript** | 6.0+ | JavaScript 超集（类型安全） |
| **Vite** | 8.0+ | 新一代前端构建工具（快速 HMR） |
| **Pinia** | 3.0+ | Vue 状态管理库（替代 Vuex） |
| **Vue Router** | 4.6+ | Vue.js 官方路由管理器 |
| **ECharts** | 5.6+ | 开源数据可视化图表库 |
| **Tailwind CSS** | 4.2+ | 实用优先的 CSS 框架 |

### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.9+ | 数据管理程序开发语言 |
| **Click** | 8.x | Python CLI 框架（命令行接口） |
| **fitparse** | 1.x | FIT 文件解析库（Garmin 设备数据格式） |
| **SQLite3** | 内置 | 轻量级关系型数据库 |

### 开发工具
- **包管理器**: npm / pnpm / yarn
- **代码编辑器**: VS Code（推荐，配合 Volar 插件）
- **版本控制**: Git + GitHub

---

## 📁 项目结构

```
sports-data-dashboard/
├── 📂 frontend/                  # 前端项目 (Vue3 + TypeScript)
│   ├── 📂 src/
│   │   ├── 📂 components/        # Vue 组件库
│   │   │   ├── 📂 common/       # 通用组件 (11个)
│   │   │   │   ├── AppHeader.vue      # 导航栏（用户信息+菜单）
│   │   │   │   ├── AppButton.vue      # 主按钮组件
│   │   │   │   ├── AppCard.vue        # 卡片容器
│   │   │   │   ├── Loading.vue        # 加载状态
│   │   │   │   ├── MetricSelector.vue # 指标选择器
│   │   │   │   ├── StatCard.vue       # 统计卡片
│   │   │   │   └── StatsPanel.vue     # 统计面板
│   │   │   ├── 📂 activities/   # 运动记录组件
│   │   │   │   └── ActivityList.vue   # 运动列表
│   │   │   └── 📂 dashboard/     # 仪表盘组件
│   │   │       ├── CalendarView.vue   # 日历热力图
│   │   │       └── ChartView.vue      # 柱形图
│   │   ├── 📂 views/             # 页面视图
│   │   │   ├── Dashboard.vue          # 仪表盘页 (/)
│   │   │   └── Activities.vue         # 运动记录页 (/activities)
│   │   ├── 📂 stores/            # Pinia 状态管理
│   │   │   └── dataStore.ts           # 数据状态 store
│   │   ├── 📂 router/            # 路由配置
│   │   ├── 📂 utils/             # 工具函数
│   │   │   └── json-reader.ts         # JSON 数据读取
│   │   ├── App.vue                   # 根组件
│   │   ├── main.ts                   # 应用入口
│   │   └── style.css                 # 全局样式 (Tailwind)
│   ├── 📂 public/
│   │   └── 📂 data/
│   │       └── data.json             # JSON 数据文件
│   ├── package.json                  # 前端依赖配置
│   ├── vite.config.ts               # Vite 配置
│   └── tsconfig.json                # TypeScript 配置
│
├── 📂 data-manager/                # 数据管理程序 (Python CLI)
│   ├── main.py                     # CLI 主程序入口 (Click)
│   ├── parser.py                   # FIT 文件解析器
│   ├── database.py                 # SQLite 数据库操作
│   ├── exporter.py                 # JSON 数据导出
│   ├── config.py                   # 配置常量
│   ├── check_fit.py                # FIT 文件检查工具
│   └── requirements.txt            # Python 依赖
│
├── 📂 data/                        # FIT 文件存储目录
│   └── 📂 2024_FIT/                # 2024 年 FIT 文件
│
├── 📂 docs/                        # 项目文档
│   ├── PRD.md                      # 产品需求规格说明书
│   ├── spec.md v2.0 ✨             # 技术规格说明书 (已更新)
│   ├── tasks.md ✨                 # 任务分解文档 (已更新)
│   ├── checklist.md ✨              # 完成清单 (已更新)
│   ├── design.md                   # 高保真设计文档
│   ├── dashboard.svg               # 仪表盘设计稿
│   └── activities.svg              # 运动记录设计稿
│
├── data.db                         # SQLite 数据库 (生成文件)
├── data.json                       # JSON 数据文件 (生成文件)
├── .gitignore                      # Git 忽略规则
├── LICENSE                         # MIT 许可证
└── README.md ✨                    # 项目说明文档 (本文件)
```

---

## 🚀 快速开始

### 环境要求

- **Node.js**: >= 16.x (推荐 18.x 或 20.x)
- **npm**: >= 8.x (或 pnpm / yarn)
- **Python**: >= 3.9 (用于数据管理程序)
- **Git**: 用于版本控制

### 1️⃣ 克隆项目

```bash
# 使用 Git 克隆仓库
git clone https://github.com/yangqun/sports-data-dashboard.git
cd sports-data-dashboard

# 或者下载 ZIP 包并解压
```

### 2️⃣ 初始化数据管理程序（Python）

```bash
# 进入项目根目录
cd sports-data-dashboard

# 进入数据管理程序目录
cd data-manager

# 创建 Python 虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# .\venv\Scripts\activate

# 安装 Python 依赖
pip install -r requirements.txt

# 初始化 SQLite 数据库
python main.py init

# 初始化用户信息（示例）
python main.py user init "yangqun" --display-name "神骏" --avatar "https://avatars.githubusercontent.com/u/26806882" --bio "练习骑行中"

# 导入 FIT 文件（将 .fit 文件放入 ../data/ 目录）
python main.py import ../data/

# 导出为 JSON 格式（供前端使用）
python main.py export

# 查看统计信息（可选）
python main.py stats

# 返回项目根目录
cd ..
```

### 3️⃣ 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装 npm 依赖（首次运行需要）
npm install

# 或使用 pnpm（更快）
# pnpm install

# 或使用 yarn
# yarn install
```

### 4️⃣ 启动开发服务器

```bash
# 启动 Vite 开发服务器（默认端口 5173）
npm run dev

# 或指定端口
npm run dev -- --port 3000
```

打开浏览器访问：
- **本地访问**: http://localhost:5173
- **仪表盘页面**: http://localhost:5173/
- **运动记录页**: http://localhost:5173/activities

### 5️⃣ 构建生产版本

```bash
# 构建生产环境静态文件（输出到 dist/ 目录）
npm run build

# 预览生产构建结果
npm run preview
```

---

## 💻 CLI 命令参考（数据管理程序）

所有命令需要在 `data-manager/` 目录下执行，且已激活 Python 虚拟环境。

### 数据库管理

```bash
# 初始化数据库（创建表结构）
python main.py init [--output ./data.db]

# 验证数据完整性
python main.py validate [--input ./data.db]
```

### FIT 文件导入

```bash
# 导入指定目录下的所有 FIT 文件
python main.py import ./data/2024_FIT/ [--output ./data.db]

# 导入单个 FIT 文件
python main.py import ./data/sample.fit [--output ./data.db]
```

**支持的文件格式**: `.fit` (Garmin/Coros 等设备导出的运动数据)

**支持的运动类型**:
| FIT 原始值 | 存储值 | 中文名称 |
|-----------|--------|---------|
| cycling | cycling | 骑行 |
| running | running | 跑步 |
| swimming | swimming | 游泳 |
| walking | walking | 健走 |
| hiking | hiking | 徒步 |
| 其他 | other | 其他 |

### 数据导出

```bash
# 导出为 JSON（标准格式）
python main.py export [--input ./data.db] [--output ./data.json]

# 导出为压缩 JSON（移除空格换行）
python main.py export --minify [--output ./data.json]
```

### 统计信息

```bash
# 查看整体统计信息
python main.py stats [--input ./data.db]

# 输出示例：
# 总活动数: 558
# 总距离: 12,345.67 km
# 总时长: 123:45:67
# 总热量: 45,678 kcal
# 运动类型分布:
#   - cycling: 450 次
#   - running: 80 次
#   - swimming: 20 次
#   ...
```

### 用户管理

```bash
# 初始化用户信息
python main.py user init "username" \
  --display-name "显示名称" \
  --avatar "https://example.com/avatar.png" \
  --bio "个人简介" \
  [--output ./data.db]

# 查看当前用户信息
python main.py user show [--output ./data.db]

# 更新用户信息（可选择性更新部分字段）
python main.py user update "username" \
  --display-name "新的显示名" \
  --bio "新的简介" \
  [--output ./data.db]

# 删除用户信息（需要确认）
python main.py user delete [--output ./data.db]
```

### 运动数据管理

```bash
# 查看单条运动详情
python main.py activity show <activity_id> [--input ./data.db]

# 删除单条运动记录（需要确认）
python main.py activity delete <activity_id> [--input ./data.db]

# 按日期范围删除运动记录（需要 --confirm 标志）
python main.py activity delete-range \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --confirm \
  [--input ./data.db]
```

### 辅助工具

```bash
# 检查 FIT 文件内容（独立脚本）
python check_fit.py <fit_file_path>

# 输出示例：
# 文件: sample.fit
# 大小: 123 KB
# 运动类型: cycling
# 开始时间: 2024-03-26 08:50:03
# 持续时间: 1697 秒
# 距离: 8113.12 米
# 可用字段: distance, duration, calories, speed, heart_rate, cadence, power, elevation
```

### 获取帮助

```bash
# 查看主命令帮助
python main.py --help

# 查看子命令帮助
python main.py import --help
python main.py export --help
python main.py user --help
python main.py activity --help
```

---

## 📊 数据模型

### 用户信息 (User)

```typescript
interface UserData {
  id: number;              // 用户唯一标识（自增主键）
  username: string;        // 用户名（唯一）
  display_name: string;    // 显示名称（可选）
  avatar_url: string;      // 头像 URL（可选）
  bio: string;             // 个人简介（可选，默认"运动爱好者"）
}
```

### 运动数据 (Activity)

```typescript
interface ActivityData {
  id: number;              // 活动唯一标识（自增主键）
  activity_type: string;   // 运动类型枚举
  start_time: string;      // 开始时间（ISO 格式）
  duration: number;        // 持续时间（秒）
  distance: number;        // 运动距离（米）
  calories: number;        // 消耗热量（kcal）
  max_speed: number;       // 最大速度（米/秒）
  avg_speed: number;       // 平均速度（米/秒）
  max_heart_rate: number;  // 最大心率（bpm，可选）
  avg_heart_rate: number;  // 平均心率（bpm，可选）
  max_cadence: number;     // 最大踏频（rpm，可选）
  avg_cadence: number;     // 平均踏频（rpm，可选）
  max_power: number;       // 最大功率（W，可选）
  avg_power: number;       // 平均功率（W，可选）
  normalized_power: number;// 标准化功率（W，可选）
  elevation_gain: number;  // 爬升海拔（米，可选）
}
```

**注意**: 心率、踏频、功率、海拔等字段为**可选字段**，根据 FIT 文件是否包含相应数据而定。缺失时值为 `null`。

---

## 🎨 设计规范

本项目遵循统一的设计语言，详见 [design.md](docs/design.md) 高保真设计文档。

### 配色方案

**品牌色**:
- 主色: `#8B5CF6` (紫色) / Light: `#A78BFA` / Dark: `#7C3AED`
- 强调色: `#F97316` (橙色) / Light: `#FB923C` / Dark: `#EA580C`
- 渐变: `linear-gradient(135deg, #8B5CF6 0%, #F97316 100%)`

**功能色**:
- 成功: `#10B981` (绿色) | 警告: `#F59E0B` (黄色)
- 错误: `#EF4444` (红色) | 信息: `#3B82F6` (蓝色)

**日历图色阶** (7 级):
| 级别 | 颜色 | 含义 |
|------|------|------|
| Level 0 | `#F3F4F6` | 无数据 |
| Level 1 | `#DBEAFE` | 低 |
| Level 2 | `#93C5FD` | 中低 |
| Level 3 | `#3B82F6` | 中 |
| Level 4 | `#2563EB` | 高 |
| Level 5 | `#1E40AF` | 极高 |
| 今天 | 红色边框 + 半透明背景 | 当前日期 |

**运动类型配色**:
- 骑行: `#8B5CF6` (紫色) | 跑步: `#F97316` (橙色)
- 游泳: `#3B82F6` (蓝色) | 健走: `#10B981` (绿色)
- 徒步: `#84CC16` (黄绿) | 其他: `#9CA3AF` (灰色)

### 响应式断点

| 断点 | 宽度范围 | 适用场景 |
|------|---------|---------|
| `sm` | >= 640px | 大屏手机 |
| `md` | >= 768px | 平板电脑 |
| `lg` | >= 1024px | 小屏笔记本 |
| `xl` | >= 1280px | 桌面显示器 |
| `2xl` | >= 1536px | 大屏显示器 |

---

## 📖 详细文档

项目包含完整的技术文档体系，位于 `docs/` 目录：

| 文档 | 说明 | 状态 |
|------|------|------|
| [PRD.md](docs/PRD.md) | 产品需求规格说明书 | ✅ 完成 |
| [spec.md](docs/spec.md) | 技术规格说明书 (v2.0) | ✨ 已更新 |
| [tasks.md](docs/tasks.md) | 任务分解与进度跟踪 | ✨ 已更新 |
| [checklist.md](docs/checklist.md) | 项目完成清单 (90%) | ✨ 已更新 |
| [design.md](docs/design.md) | UI/UX 高保真设计规范 | ✅ 完成 |
| [COMPLETION_SUMMARY.md](docs/COMPLETION_SUMMARY.md) | 用户使用手册 | ✅ 完成 |

---

## 📈 当前进度 & 完成度

**最后更新**: 2026-04-08  
**整体完成度**: **~90%** 🎉

### ✅ 已完成的核心功能（P0 必需）

#### 数据管理层 (100%)
- ✅ Python CLI 程序完整实现（init/import/export/stats/validate/user/activity 命令）
- ✅ FIT 文件解析器（fitparse 库，支持 6 种运动类型，16 个数据字段）
- ✅ SQLite 数据库操作（CRUD、去重、统计、按范围删除）
- ✅ JSON 数据导出（支持 minify 压缩输出）
- ✅ 用户管理和运动数据管理完整功能

#### 前端层 (95%)
- ✅ Vue3 + TypeScript + Vite 项目架构（现代化技术栈）
- ✅ 完整的组件库（11 个核心组件）
- ✅ Pinia 状态管理（dataStore 完整实现，TypeScript 类型安全）
- ✅ ECharts 图表集成（日历热力图 + 柱形图统计）
- ✅ 响应式布局（Tailwind CSS 4.2+，5 个断点适配）
- ✅ Vue Router 路由（懒加载，2 个主要页面）
- ✅ 数据读取层（JSON reader with TypeScript interfaces）

#### 文档层 (95%)
- ✅ 7 份核心文档齐全（PRD/spec/tasks/checklist/design/README/手册）
- ✅ spec.md 升级至 v2.0（反映实际代码实现）
- ✅ tasks.md 和 checklist.md 同步更新

### 🔄 进行中的工作（10%）

- **样式细节优化**: 移动端完美适配、暗色模式（可选增强）
- **交互体验提升**: 页面过渡动画、骨架屏加载状态、错误提示组件

### ⏳ 待实施的功能（P1/P2 可选增强）

#### 工程化（重要但不紧急）
- [ ] **GitHub Actions CI/CD**: 自动化数据更新流水线（定时触发 + 手动触发）
- [ ] **测试框架集成**: Vitest 单元测试 + Vue Test Utils 组件测试
- [ ] **代码质量工具**: ESLint + Prettier 代码规范检查

#### 性能优化（建议实施）
- [ ] **虚拟滚动**: ActivityList 大列表性能优化（1000+ 条记录）
- [ ] **ECharts 按需引入**: 减少打包体积（当前全量引入 ~1MB）
- [ ] **图片懒加载**: 用户头像 CDN 加速 + 懒加载策略
- [ ] **数据压缩**: Gzip/Brotli 静态资源压缩

#### 生产部署（上线必需）
- [ ] **静态托管配置**: GitHub Pages / Netlify / Vercel 三选一
- [ ] **域名 + DNS**: 自定义域名绑定（可选）
- [ ] **HTTPS 配置**: SSL 证书（托管平台通常自动提供）
- [ ] **监控告警**: Sentry 错误追踪 + Core Web Vitals 监控

#### 扩展功能（远期规划）
- [ ] **地图轨迹展示**: Leaflet / Mapbox 集成（导航入口已预留）
- [ ] **多数据源导入**: CSV/GPX/TCX 手动上传功能
- [ ] **数据对比功能**: 多时段数据对比视图
- [ ] **PWA 支持**: 离线访问 + 添加到主屏幕
- [ ] **社交功能**: 数据分享链接 / 图片导出

---

## 🤝 贡献指南

欢迎贡献代码、报告 Bug 或提出功能请求！

### 如何贡献

1. **Fork 项目** → 点击右上角 Fork 按钮
2. **克隆 Fork** → `git clone https://github.com/<your-username>/sports-data-dashboard.git`
3. **创建分支** → `git checkout -b feature/amazing-feature`
4. **提交更改** → `git commit -m 'Add some amazing feature'`
5. **推送分支** → `git push origin feature/amazing-feature`
6. **创建 Pull Request** → 在 GitHub 上提交 PR

### 代码风格

- **前端**: TypeScript 严格模式，ESLint 规则（待配置），Prettier 格式化
- **后端**: PEP 8 规范，Black 格式化（可选）
- **提交信息**: 遵循 Conventional Commits 规范（feat/fix/docs/refactor/test/chore）

### 报告 Bug

请使用 [GitHub Issues](../../issues) 提交 Bug 报告，包含以下信息：
- **问题描述**: 清晰描述 Bug 表现
- **复现步骤**: 如何重现该问题
- **预期行为**: 期望的正确行为
- **环境信息**: 操作系统、浏览器/Node 版本、错误日志截图

### 功能请求

欢迎提出新功能建议！请在 Issue 中详细描述：
- **功能背景**: 为什么需要这个功能
- **使用场景**: 具体的使用例子
- **参考设计**: 如果有原型图或参考链接请附上

---

## 📄 许可证

本项目采用 **MIT License** 开源协议。详见 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2026 yangqun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 致谢

感谢以下开源项目和社区：

- **[Vue.js](https://vuejs.org/)** - 渐进式 JavaScript 框架
- **[Vite](https://vitejs.dev/)** - 下一代前端构建工具
- **[ECharts](https://echarts.apache.org/)** - 强大的数据可视化库
- **[Tailwind CSS](https://tailwindcss.com/)** - 实用优先的 CSS 框架
- **[Pinia](https://pinia.vuejs.org/)** - 直观的 Vue 状态管理
- **[Click](https://click.palletsprojects.com/)** - Python CLI 框架
- **[fitparse](https://github.com/dtcooper/python-fitparse)** - FIT 文件解析库
- **[Heroicons](https://heroicons.com/)** - 精美的 SVG 图标库

---

## 📮 联系方式

- **作者**: yangqun
- **GitHub**: [@yangqun](https://github.com/conanyangqun)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

---

## 🗺️ 路线图（Roadmap）

### 近期计划（1-2 周）
- [ ] 配置 GitHub Actions 自动化数据更新工作流
- [ ] 添加 Vitest 测试框架，为核心逻辑编写单元测试
- [ ] 完成本次文档更新（✨ 本次已完成 spec/tasks/checklist/README）

### 短期目标（1 个月内）
- [ ] 完成生产环境部署（GitHub Pages 或 Netlify）
- [ ] 优化性能（虚拟滚动、ECharts 按需引入）
- [ ] 添加基本的手动测试覆盖（跨浏览器验证）

### 中期规划（3 个月）
- [ ] 完善测试覆盖率（目标 70%+ 单元测试 + 集成测试）
- [ ] 添加地图轨迹展示功能（Leaflet/Mapbox 集成）
- [ ] 支持手动上传其他格式数据（CSV/GPX/TCX）
- [ ] PWA 支持（离线访问 + 安装提示）

### 远期愿景（6-12 个月）
- [ ] 多用户支持（本地存储多套用户数据）
- [ ] 数据分享功能（生成分享链接/图片卡片）
- [ ] 目标设定和达成率追踪
- [ ] 社交功能（评论、点赞、关注）
- [ ] 移动端原生应用（ Capacitor / React Native）

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

Made with ❤️ by [yangqun](https://github.com/conanyangqun)

[⬆ 回到顶部](#sports-data-dashboard--️‍♂️-)

</div>
