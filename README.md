# sports-data-dashboard

运动数据仪表盘 - 基于Vue3的运动数据可视化展示平台。

## 项目概述

本项目旨在开发一个运动数据展示网站，用于运动数据的可视化。数据管理作为独立程序运行，可以在本地或GitHub Actions中执行。

## 技术栈

- 前端框架：Vue 3
- 构建工具：Vite
- 数据可视化：ECharts
- 数据管理程序：Python
- 数据库：SQLite3
- FIT文件解析：fitparse库

## 项目结构

```
sports-data-dashboard/
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── views/         # 页面视图
│   │   ├── stores/        # 状态管理
│   │   └── utils/         # 工具函数
│   ├── public/
│   │   └── data/          # 数据文件目录
│   │       ├── data.json  # JSON数据文件
│   │       └── data.db    # SQLite数据库文件
│   └── package.json
├── data-manager/          # 数据管理程序
│   ├── main.py           # 主程序入口
│   ├── parser.py         # FIT文件解析器
│   ├── database.py       # 数据库操作
│   ├── exporter.py       # 数据导出
│   └── config.py         # 配置文件
├── fit-files/            # FIT文件存储目录
├── docs/                 # 文档
│   ├── requirements.md   # 需求规格说明书
│   ├── spec.md          # 技术规格说明书
│   ├── tasks.md         # 任务分解
│   └── checklist.md     # 完成清单
└── README.md
```

## 功能特性

### 数据管理程序

- FIT文件解析：支持解析运动类型、时间、距离、心率、踏频、功率、海拔等数据
- 数据库管理：SQLite数据库存储，支持CRUD操作
- 数据导出：支持导出为JSON格式
- 用户管理：支持用户信息的初始化、查看和更新
- CLI命令：提供命令行接口进行数据管理

### 前端（开发中）

- Vue3 + Vite：现代化的前端开发框架
- 数据可视化：使用ECharts展示运动数据
- 响应式设计：支持多设备访问
- 用户信息展示：头像、用户名、简介及最近1周运动统计
- 日历图：年度运动数据可视化，支持多种着色方式（距离/时长/次数/热量/平均速度）
- 柱形图：多维度数据分析（周/月/年/全部模式），支持指标切换
- 运动列表：详细运动记录展示，支持排序和筛选

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 数据管理程序使用

1. 创建Python虚拟环境：
```bash
cd data-manager
python3 -m venv venv
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
python main.py init
```

4. 初始化用户信息：
```bash
python main.py user init "your_username" --avatar "avatar_url" --bio "your_bio"
```

5. 导入FIT文件：
```bash
python main.py import ../fit-files/
```

6. 导出JSON数据：
```bash
python main.py export
```

7. 查看统计信息：
```bash
python main.py stats
```

### 前端开发

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

## CLI命令

### 数据库管理

```bash
python main.py init [--output path]
```

### FIT文件导入

```bash
python main.py import <fit_dir> [--output path]
```

### 数据导出

```bash
python main.py export [--input path] [--output path]
```

### 统计信息

```bash
python main.py stats [--input path]
```

### 用户管理

```bash
# 初始化用户信息
python main.py user init <username> [--avatar url] [--bio text]

# 查看用户信息
python main.py user show [username]

# 更新用户信息
python main.py user update <username> [--avatar url] [--bio text]
```

## 数据格式

### FIT文件支持

支持的运动类型：
- running (跑步)
- cycling (骑行)
- swimming (游泳)
- walking (健走)
- hiking (徒步)
- other (其他)

### 数据字段

运动数据包含以下字段：
- activity_type: 运动类型
- start_time: 开始时间
- duration: 持续时间（秒）
- distance: 距离（米）
- calories: 卡路里
- max_speed: 最大速度（米/秒）
- avg_speed: 平均速度（米/秒）
- max_heart_rate: 最大心率（可选）
- avg_heart_rate: 平均心率（可选）
- max_cadence: 最大踏频（可选）
- avg_cadence: 平均踏频（可选）
- max_power: 最大功率（可选）
- avg_power: 平均功率（可选）
- normalized_power: 标准化功率（可选）
- elevation_gain: 爬升海拔（可选）

## 开发进度

### 第一阶段：项目初始化和基础架构 ✅
- [x] 项目结构搭建
- [x] 前端项目初始化
- [x] 数据管理程序初始化

### 第二阶段：数据管理程序开发 ✅
- [x] FIT文件解析器
- [x] 数据库操作模块
- [x] 数据导出模块
- [x] CLI命令实现
- [x] 用户管理功能

### 第三阶段：前端核心功能开发 🚧
- [ ] 基础组件开发（Header、Loading、ErrorBoundary等）
- [ ] 数据读取层（SQLite/JSON数据读取）
- [ ] 状态管理（Pinia dataStore）
- [ ] 用户信息模块（头像、简介、最近1周统计）
- [ ] 日历视图（年份切换、5种着色方式）
- [ ] 柱形图视图（4种模式、指标切换、动态横轴）
- [ ] 运动列表（表格展示、排序、筛选、分页）
- [ ] 路由和页面集成

## 文档

详细的项目文档请查看 [docs/](docs/) 目录：
- [PRD.md](docs/PRD.md) - 产品需求规格说明书
- [spec.md](docs/spec.md) - 技术规格说明书
- [tasks.md](docs/tasks.md) - 任务分解
- [checklist.md](docs/checklist.md) - 完成清单

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！
