# 运动数据仪表盘技术规格说明书

## 一、项目概述

### 1.1 项目目标
开发一个基于Vue3的运动数据展示网站，实现运动数据的可视化展示。数据管理作为独立程序运行，可以在本地或GitHub Actions中执行。

### 1.2 技术栈
- **前端框架：** Vue 3.5+ (Composition API + `<script setup>`)
- **编程语言：** TypeScript 6.0+
- **构建工具：** Vite 8.0+
- **状态管理：** Pinia 3.0+
- **路由：** Vue Router 4.6+
- **数据可视化：** ECharts 5.6+
- **样式方案：** Tailwind CSS 4.2+
- **数据管理程序：** Python 3.9+
- **CLI 框架：** Click
- **数据库：** SQLite3 或 JSON文件
- **FIT文件解析：** fitparse库

## 二、系统架构

### 2.1 整体架构
```
┌─────────────────────────────────────────┐
│         前端 (Vue3 静态网站)             │
│  - TypeScript + Composition API         │
│  - 数据展示 (直接读取 JSON 数据文件)     │
│  - 用户交互                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      数据文件 (JSON)                     │
│  - frontend/public/data/data.json       │
│  - 运动数据                              │
│  - 用户信息                              │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    数据管理程序 (Python CLI 工具)       │
│  - FIT文件解析                          │
│  - SQLite 数据库存储                    │
│  - JSON 数据导出                        │
│  - 用户管理和运动数据 CRUD              │
└─────────────────────────────────────────┘
```

### 2.2 目录结构
```
sports-data-dashboard/
├── frontend/                  # 前端项目 (Vue3 + TypeScript + Vite)
│   ├── src/
│   │   ├── components/        # Vue 组件
│   │   │   ├── common/       # 通用组件
│   │   │   │   ├── AppHeader.vue      # 导航栏组件
│   │   │   │   ├── AppButton.vue      # 按钮组件
│   │   │   │   ├── AppCard.vue        # 卡片容器组件
│   │   │   │   ├── Loading.vue        # 加载状态组件
│   │   │   │   ├── MetricSelector.vue # 指标选择器组件
│   │   │   │   ├── StatCard.vue       # 统计卡片组件
│   │   │   │   └── StatsPanel.vue     # 统计面板组件
│   │   │   ├── activities/   # 运动记录相关组件
│   │   │   │   └── ActivityList.vue   # 运动列表组件
│   │   │   └── dashboard/     # 仪表盘相关组件
│   │   │       ├── CalendarView.vue   # 日历热力图组件
│   │   │       └── ChartView.vue      # 柱形图组件
│   │   ├── views/             # 页面视图
│   │   │   ├── Dashboard.vue          # 仪表盘页面
│   │   │   └── Activities.vue         # 运动记录页面
│   │   ├── stores/            # Pinia 状态管理
│   │   │   └── dataStore.ts           # 数据状态管理
│   │   ├── router/            # Vue Router 路由配置
│   │   │   └── index.ts
│   │   ├── utils/             # 工具函数
│   │   │   └── json-reader.ts         # JSON 数据读取模块
│   │   ├── App.vue             # 根组件
│   │   ├── main.ts             # 应用入口
│   │   └── style.css           # 全局样式
│   ├── public/
│   │   ├── data/
│   │   │   └── data.json      # JSON 数据文件（当前使用）
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── data-manager/              # 数据管理程序 (Python)
│   ├── main.py               # CLI 主程序入口（Click 框架）
│   ├── parser.py             # FIT 文件解析器
│   ├── database.py           # SQLite 数据库操作
│   ├── exporter.py           # 数据导出为 JSON
│   ├── config.py             # 配置管理
│   ├── check_fit.py          # FIT 文件检查工具
│   └── requirements.txt      # Python 依赖
├── data/                     # FIT 文件存储目录
│   └── 2024_FIT/             # 2024 年的 FIT 文件
├── docs/                     # 项目文档
│   ├── design.md             # 高保真设计文档
│   ├── PRD.md                # 产品需求规格说明书
│   ├── spec.md               # 技术规格说明书（本文件）
│   ├── tasks.md              # 任务分解
│   ├── checklist.md          # 完成清单
│   ├── dashboard.svg         # 仪表盘页面设计稿
│   └── activities.svg        # 运动记录页面设计稿
├── archive/                  # 归档文件
├── data.db                   # SQLite 数据库文件（生成）
├── data.json                 # JSON 数据文件（生成，用于前端）
├── .gitignore
├── LICENSE
└── README.md
```

## 三、数据模型设计

### 3.1 用户信息
```json
{
    "user": {
        "id": 2,
        "username": "yangqun",
        "display_name": "神骏",
        "avatar_url": "https://avatars.githubusercontent.com/u/26806882",
        "bio": "练习骑行中"
    }
}
```

**字段说明：**
- `id`: 用户唯一标识（整数，自增主键）
- `username`: 用户名（字符串，唯一）
- `display_name`: 显示名称（字符串，可选）
- `avatar_url`: 头像 URL（字符串，可选）
- `bio`: 个人简介（字符串，可选）

### 3.2 运动数据
```json
{
    "activities": [
        {
            "id": 558,
            "activity_type": "cycling",
            "start_time": "2026-03-26 08:50:03",
            "duration": 1697.0,
            "distance": 8113.12,
            "calories": 142.0,
            "max_speed": 6.582,
            "avg_speed": 4.78,
            "max_heart_rate": null,
            "avg_heart_rate": null,
            "max_cadence": null,
            "avg_cadence": null,
            "max_power": null,
            "avg_power": null,
            "normalized_power": null,
            "elevation_gain": 5.0
        }
    ]
}
```

**字段说明：**
- `id`: 活动唯一标识（整数，自增主键）
- `activity_type`: 运动类型（枚举：cycling, running, swimming, walking, hiking, other）
- `start_time`: 开始时间（ISO 格式日期时间字符串）
- `duration`: 持续时间（秒，浮点数）
- `distance`: 运动距离（米，浮点数）
- `calories`: 消耗热量（kcal，浮点数）
- `max_speed`: 最大速度（米/秒，浮点数，可选）
- `avg_speed`: 平均速度（米/秒，浮点数，可选）
- `max_heart_rate`: 最大心率（bpm，整数，可选）
- `avg_heart_rate`: 平均心率（bpm，整数，可选）
- `max_cadence`: 最大踏频（rpm，整数，可选）
- `avg_cadence`: 平均踏频（rpm，整数，可选）
- `max_power`: 最大功率（W，整数，可选）
- `avg_power`: 平均功率（W，整数，可选）
- `normalized_power`: 标准化功率（W，整数，可选）
- `elevation_gain`: 爬升海拔（米，浮点数，可选）

**注意：** 心率、踏频、功率等字段为可选字段，根据 FIT 文件中是否包含相应数据而定。如果 FIT 文件中没有这些数据，对应字段将为 `null`。

### 3.3 SQLite 表结构

#### 3.3.1 用户信息表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100),
    avatar_url VARCHAR(255),
    bio TEXT
);
```

#### 3.3.2 运动数据表 (activities)
```sql
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    duration REAL,
    distance REAL,
    calories REAL,
    max_speed REAL,
    avg_speed REAL,
    max_heart_rate INTEGER,
    avg_heart_rate INTEGER,
    max_cadence INTEGER,
    avg_cadence INTEGER,
    max_power INTEGER,
    avg_power INTEGER,
    normalized_power INTEGER,
    elevation_gain REAL
);
```

## 四、数据管理程序设计

### 4.1 程序架构
```
data-manager/
├── main.py               # CLI 主程序入口（Click 框架）
├── parser.py             # FIT 文件解析器（fitparse 库）
├── database.py           # SQLite 数据库操作类
├── exporter.py           # 数据导出为 JSON
├── config.py             # 配置常量
├── check_fit.py          # FIT 文件检查工具
└── requirements.txt      # Python 依赖列表
```

### 4.2 CLI 命令接口

#### 4.2.1 初始化数据库
```bash
python main.py init [--output path]
```

#### 4.2.2 导入 FIT 文件
```bash
python main.py import <fit_dir> [--output path]
```
- 支持批量导入指定目录下的所有 `.fit` 文件
- 自动跳过重复数据（基于 start_time 去重）

#### 4.2.3 导出为 JSON
```bash
python main.py export [--input path] [--output path] [--minify]
```
- `--minify`: 压缩 JSON 输出（移除空格和换行）

#### 4.2.4 查看统计信息
```bash
python main.py stats [--input path]
```

#### 4.2.5 验证数据完整性
```bash
python main.py validate [--input path]
```

#### 4.2.6 用户管理命令组 (`user`)
```bash
# 初始化用户信息
python main.py user init <username> [--display-name name] [--avatar url] [--bio text] [--output path]

# 查看用户信息
python main.py user show [username] [--output path]

# 更新用户信息
python main.py user update <username> [--display-name name] [--avatar url] [--bio text] [--output path]

# 删除用户信息（需确认）
python main.py user delete [--output path]
```

#### 4.2.7 运动数据管理命令组 (`activity`)
```bash
# 查看运动详情
python main.py activity show <activity_id> [--input path]

# 删除单条运动记录（需确认）
python main.py activity delete <activity_id> [--input path]

# 按日期范围删除运动记录（需确认）
python main.py activity delete-range --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--input path] [--confirm]
```

### 4.3 FIT 文件解析规范

#### 4.3.1 解析流程
1. 使用 fitparse 库读取 FIT 文件
2. 验证文件格式有效性
3. 提取运动类型（sport 字段映射）
4. 提取开始时间（start_time 或 timestamp 字段）
5. 提取持续时间（total_timer_time 字段）
6. 提取距离（total_distance 字段）
7. 提取卡路里（total_calories 字段）
8. 提取速度数据（enhanced_max_speed, enhanced_avg_speed 字段）
9. 提取心率数据（max_heart_rate, avg_heart_rate）- 可选
10. 提取踏频数据（max_cadence, avg_cadence）- 可选
11. 提取功率数据（max_power, avg_power, normalized_power）- 可选
12. 提取海拔数据（total_ascent -> elevation_gain）- 可选
13. 保存到数据库（不存在的数据字段设为 NULL）

#### 4.3.2 支持的运动类型映射
| FIT sport 值 | 存储值 | 中文显示 |
|-------------|--------|---------|
| cycling | cycling | 骑行 |
| running | running | 跑步 |
| swimming | swimming | 游泳 |
| walking | walking | 健走 |
| hiking | hiking | 徒步 |
| 其他 | other | 其他 |

#### 4.3.3 数据字段映射
```python
FIT 字段 -> 数据库字段
sport -> activity_type
timestamp / start_time -> start_time
total_timer_time -> duration
total_distance -> distance
total_calories -> calories
enhanced_max_speed -> max_speed
enhanced_avg_speed -> avg_speed
max_heart_rate -> max_heart_rate (可选)
avg_heart_rate -> avg_heart_rate (可选)
max_cadence -> max_cadence (可选)
avg_cadence -> avg_cadence (可选)
max_power -> max_power (可选)
avg_power -> avg_power (可选)
normalized_power -> normalized_power (可选)
total_ascent -> elevation_gain (可选)
```

### 4.4 数据导出格式

导出的 JSON 格式与 [3.2 运动数据](#32-运动数据) 节定义一致。当前前端使用此 JSON 文件作为数据源。

## 五、前端组件设计

### 5.1 应用结构
```
App.vue (根组件)
├── AppHeader.vue              # 全局导航栏（用户信息 + 菜单）
├── <RouterView>              # 路由视图容器
│   ├── Dashboard.vue         # 仪表盘页面 (/)
│   │   ├── StatsPanel.vue    # 周/周期统计面板（左侧 1/4）
│   │   ├── CalendarView.vue  # 日历热力图（右侧 3/4）
│   │   └── ChartView.vue     # 柱形图统计视图（底部全宽）
│   └── Activities.vue        # 运动记录页面 (/activities)
│       └── ActivityList.vue  # 运动数据表格
```

### 5.2 页面路由
```typescript
// frontend/src/router/index.ts
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/activities',
    name: 'Activities',
    component: () => import('@/views/Activities.vue')
  }
]
```

### 5.3 核心组件详细说明

#### 5.3.1 AppHeader.vue（导航栏组件）
**功能：**
- 显示用户头像（支持 URL 和首字母占位符两种模式）
- 显示用户显示名称（display_name）或用户名（username）
- 显示用户简介（bio），默认值为"运动爱好者"
- 导航菜单：仪表盘、运动记录、地图
- 地图菜单点击时提示"地图页面正在开发中，敬请期待！"

**样式规格：**
- 高度：80px
- 背景：渐变色 `linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)`
- 内边距：左右各 40px
- 响应式：768px 以下隐藏简介文字，调整内边距

#### 5.3.2 Dashboard.vue（仪表盘页面）
**布局结构：**
```
┌─────────────────────────────────────────────┐
│  AppHeader（导航栏）                         │
├──────────────────┬──────────────────────────┤
│                  │                          │
│  StatsPanel      │  CalendarView            │
│  （周统计数据）   │  （日历热力图）           │
│  （宽度 25%）     │  （宽度 75%）            │
│                  │                          │
├──────────────────┴──────────────────────────┤
│                                             │
│  ChartView（柱形图统计视图，全宽）            │
│                                             │
└─────────────────────────────────────────────┘
```

**功能：**
- 上半部分左侧：最近 1 周运动统计（总距离、总时长、总次数、总热量、平均速度）
- 显示本周日期范围标签（MM/DD - MM/DD 格式，周一作为一周起始）
- 上半部分右侧：日历热力图
- 下半部分：柱形图统计视图
- 响应式：1024px 以下改为上下堆叠布局

#### 5.3.3 CalendarView.vue（日历热力图组件）
**功能特性：**
- 使用 ECharts 日历图（heatmap）展示年度运动数据
- 年份切换：
  - 左右箭头按钮切换年份
  - 点击年份输入框弹出年份选择器弹窗（Teleport to body）
  - 弹窗采用 3 列网格布局，每页显示 12 个年份
  - 顶部导航支持翻页，显示当前页年份范围
  - 当前选中年份蓝色高亮
  - 点击外部区域自动关闭弹窗
- 默认显示数据中最新一年的数据
- 指标切换（MetricSelector）：距离、时长、次数、热量、平均速度
- 今天标记：红色边框突出显示，图例包含"今天"说明
- 鼠标悬停显示 Tooltip（日期 + 数值 + "(今天)"标记）
- 图例：无数据、低、中低、中、高、极高、今天（共 7 级）
- 指标选择器垂直排列在日历图左侧

**颜色强度映射（以距离为例）：**
| 级别 | 颜色 | 说明 |
|------|------|------|
| Level 0 | #F3F4F6 | 无数据 |
| Level 1 | #DBEAFE | 低 |
| Level 2 | #93C5FD | 中低 |
| Level 3 | #3B82F6 | 中 |
| Level 4 | #2563EB | 高 |
| Level 5 | #1E40AF | 极高 |
| 今天 | rgba(239, 68, 68, 0.3) + 红色边框 | 今天 |

#### 5.3.4 ChartView.vue（柱形图统计视图组件）
**功能特性：**
- 使用 ECharts 柱形图（bar）展示运动数据统计
- 四种显示模式切换：周、月、年、全部
- 每种模式包含：
  - 数据统计卡片（StatsPanel）：按对应周期统计总距离、总时长、总次数、总热量、平均速度
  - 指标选择器（MetricSelector）：纵轴指标可切换（距离、时长、次数、热量、平均速度）
  - 柱形图可视化
  - 翻页组件（仅周/月/年模式）

**横轴配置：**
| 模式 | 横轴单位 | 翻页标签格式 |
|------|---------|------------|
| 周 | 天 (MM/DD) | MM/DD - MM/DD |
| 月 | 天 (MM/DD) | YYYY/MM |
| 年 | 月 (1月-12月) | YYYY 年 |
| 全部 | 年 (YYYY) | YYYY - YYYY |

**数据格式规范：**
- 次数指标：显示为整数
- 其他指标：保留一位小数
- Y 轴名称加粗显示，颜色更深

**翻页功能：**
- 周模式：按周偏移翻页，显示当前周的日期范围（周一作为一周起始）
- 月模式：按月偏移翻页，显示当前月份
- 年模式：按年份切换，显示当前年份
- 全部模式：显示整个运动生涯的时间范围，不支持翻页

#### 5.3.5 ActivityList.vue（运动列表组件）
**功能特性：**
- 表格形式展示运动数据
- 11 个数据列：
  1. 运动日期（格式化为 YYYY-MM-DD）
  2. 运动类型（中文显示：骑行、跑步、游泳、健走、徒步、其他）
  3. 运动距离（单位：km，保留 2 位小数）
  4. 运动时长（格式化为 HH:MM:SS）
  5. 热量（单位：kcal）
  6. 平均速度（单位：km/h，保留 1 位小数）
  7. 最大速度（单位：km/h，保留 1 位小数）
  8. 平均心率（单位：bpm，null 显示为 "-"）
  9. 最大心率（单位：bpm，null 显示为 "-"）
  10. 平均踏频（单位：rpm，null 显示为 "-"）
  11. 最大踏频（单位：rpm，null 显示为 "-"）

**交互功能：**
- 分页：默认每页显示固定条数，支持页码跳转
- 排序：默认按日期倒序排列，点击表头可切换升序/降序
- 筛选：支持按运动类型筛选（下拉框）
- 空数据显示："暂无数据"提示
- 分页信息显示："显示 X-Y 条，共 Z 条"

#### 5.3.6 通用组件

**StatsPanel.vue（统计面板组件）**
- 展示一组 StatCard 组件
- 支持 `variant` 属性：`default`（标准尺寸）或 `mini`（紧凑尺寸）
- 可选标题参数

**StatCard.vue（统计卡片组件）**
- 显示图标、指标名称、指标值
- 支持渐变背景色配置
- 5 种预设配色方案（对应不同指标类型）

**MetricSelector.vue（指标选择器组件）**
- 垂直排列的按钮组
- 支持双向绑定（v-model）
- 激活状态高亮显示
- 用于日历图和柱形图的指标切换

**AppCard.vue（卡片容器组件）**
- 统一的卡片容器样式
- 圆角、阴影、边框
- 可选内边距配置

**AppButton.vue（按钮组件）**
- 主按钮样式（渐变背景）
- Hover/Active 状态动画

**Loading.vue（加载状态组件）**
- 数据加载中的占位提示

### 5.4 数据读取层

#### 5.4.1 JSON 数据读取（当前使用）
```typescript
// utils/json-reader.ts
export interface UserData {
  id: number
  username: string
  display_name: string | null
  avatar_url: string | null
  bio: string | null
}

export interface ActivityData {
  id: number
  activity_type: string
  start_time: string
  duration: number
  distance: number
  calories: number
  max_speed: number | null
  avg_speed: number | null
  max_heart_rate: number | null
  avg_heart_rate: number | null
  max_cadence: number | null
  avg_cadence: number | null
  max_power: number | null
  avg_power: number | null
  normalized_power: number | null
  elevation_gain: number | null
}

export interface SportsData {
  user: UserData | null
  activities: ActivityData[]
}

export async function loadData(): Promise<SportsData>
```

**实现方式：** 使用 `fetch('/data/data.json')` 异步加载 JSON 文件。

### 5.5 状态管理 (Pinia)

#### 5.5.1 dataStore（数据状态管理）
```typescript
// stores/dataStore.ts

// 类型定义
type DisplayMode = 'week' | 'month' | 'year' | 'all'
type ChartMetric = 'distance' | 'duration' | 'count' | 'calories' | 'avg_speed'
type CalendarMetric = 'distance' | 'duration' | 'count' | 'calories' | 'avg_speed'

// State（状态）
{
  user: UserData | null           // 用户信息
  activities: ActivityData[]      // 运动数据列表
  loading: boolean                // 加载状态
  error: string | null            // 错误信息
  currentMode: DisplayMode        // 当前显示模式（周/月/年/全部）
  currentYear: number             // 当前选中年份
  currentWeekOffset: number       // 周偏移量（用于翻页）
  currentMonthOffset: number      // 月偏移量（用于翻页）
  calendarMetric: CalendarMetric  // 日历图着色指标
  chartMetric: ChartMetric        // 柱形图纵轴指标
}

// Getters（计算属性）
{
  isLoading: boolean               // 是否正在加载
  hasError: boolean               // 是否有错误
  errorMessage: string | null     // 错误消息
}

// Actions（操作方法）
{
  loadAllData()                   // 加载所有数据（JSON 文件）
  getWeekStats(): WeekStats       // 计算最近 1 周统计数据
  processCalendarData(year, metric): CalendarDayData[]  // 处理日历图数据
  processChartData(mode, metric): { stats, data }       // 处理柱形图数据
  setDisplayMode(mode)            // 设置显示模式
  setYear(year)                   // 设置当前年份
  setCalendarMetric(metric)       // 设置日历图指标
  setChartMetric(metric)          // 设置柱形图指标
  setWeekOffset(offset)           // 设置周偏移量
  setMonthOffset(offset)          // 设置月偏移量
}
```

**WeekStats 接口：**
```typescript
interface WeekStats {
  totalDistance: number   // 总距离（米）
  totalDuration: number   // 总时长（秒）
  totalCount: number      // 总次数
  totalCalories: number   // 总热量（kcal）
  avgSpeed: number        // 平均速度（km/h）
}
```

**数据处理逻辑：**

1. **getWeekStats()**: 
   - 计算从现在往前推 7 天的数据
   - 聚合总距离、总时长、总次数、总热量
   - 计算平均速度（总距离/总时长 * 3.6 转换为 km/h）

2. **processCalendarData(year, metric)**:
   - 过滤指定年份的活动数据
   - 按日期聚合（dateMap）
   - 根据 metric 参数计算每日数值：
     - distance: 米 → 公里（÷1000）
     - duration: 秒 → 分钟（÷60）
     - count: 固定为 1
     - calories: kcal（不变）
     - avg_speed: m/s → km/h（×3.6）

3. **processChartData(mode, metric)**:
   - 根据 mode 分组活动数据：
     - week: 按天分组（周一作为一周起始）
     - month: 按天分组
     - year: 按月分组（1月-12月）
     - all: 按年分组
   - 根据 metric 聚合每组数值
   - 返回统计数据和图表数据点数组

## 六、前端路由设计

### 6.1 路由配置
```typescript
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/activities',
    name: 'Activities',
    component: () => import('@/views/Activities.vue')
  }
]
```

### 6.2 路由特点
- 使用懒加载（动态导入）优化性能
- 仅两个主要页面：仪表盘和运动记录
- 未配置路由守卫（当前无需认证）

## 七、GitHub Actions 集成（待实现）

### 7.1 自动化工作流（规划中）
```yaml
name: Update Sports Data

on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行一次
  workflow_dispatch:     # 手动触发

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install fitparse click
      - name: Initialize database
        run: |
          python data-manager/main.py init
      - name: Parse FIT files
        run: |
          python data-manager/main.py import ./fit-files/
      - name: Export to JSON
        run: |
          python data-manager/main.py export
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add frontend/public/data/
          git commit -m "Update sports data" || exit 0
          git push
```

## 八、部署方案

### 8.1 开发环境
```bash
# 前端开发服务器
cd frontend
npm run dev
# 访问 http://localhost:5173

# 数据管理
cd data-manager
python main.py init                                    # 初始化数据库
python main.py user init "username" --bio "运动爱好者"  # 初始化用户
python main.py import ../data/                           # 导入 FIT 文件
python main.py export                                   # 导出 JSON
```

### 8.2 生产环境构建
```bash
cd frontend
npm run build
# 输出目录：dist/
```

**部署方式选项：**
- GitHub Pages（推荐）
- Netlify
- Vercel
- 任意静态文件托管服务

**数据文件处理：**
- 将 `frontend/public/data/data.json` 包含在生产构建中
- 通过数据管理程序定期更新数据文件后重新部署

## 九、性能优化（部分实现）

### 9.1 已实现的优化
- ✅ 组件懒加载（路由级别）
- ✅ ECharts 图表实例复用
- ✅ 数据聚合在 store 层完成，避免重复计算

### 9.2 待实现的优化
- ⏳ 虚拟滚动（长列表优化，ActivityList 组件）
- ⏳ 数据文件压缩（gzip/brotli）
- ⏳ 图片资源优化（头像 CDN 加速）
- ⏳ ECharts 按需引入（减少包体积）

## 十、安全考虑

### 10.1 已实现的安全措施
- ✅ FIT 文件格式验证（解析前检查）
- ✅ 数据去重机制（防止重复导入）
- ✅ 数据库操作异常捕获

### 10.2 待加强的安全措施
- ⏳ 文件大小限制
- ⏳ 输入数据清理（防止 SQL 注入）
- ⏳ 敏感信息过滤（确保不泄露隐私数据）

## 十一、测试策略（待实施）

### 11.1 单元测试（计划中）
- FIT 文件解析逻辑测试
- 数据导出逻辑测试
- 数据处理逻辑测试（store 的计算函数）

### 11.2 集成测试（计划中）
- 数据导入导出流程测试
- 前端数据读取测试
- 组件渲染测试

### 11.3 E2E 测试（计划中）
- 用户操作流程测试
- 数据可视化展示测试

## 十二、配置管理

### 12.1 数据管理程序配置
```python
# config.py
DATABASE_FILE = "data.db"
JSON_FILE = "data.json"
SUPPORTED_TYPES = ["running", "cycling", "swimming", "walking", "hiking", "other"]
```

### 12.2 前端配置
```typescript
// vite.config.ts
// 当前使用默认 Vite 配置
// 开发服务器端口：5173
```

## 十三、数据更新流程

### 13.1 本地更新流程
1. 初始化数据库：`python data-manager/main.py init`
2. 初始化用户信息：`python data-manager/main.py user init "username" --display-name "显示名" --avatar "头像URL" --bio "个人简介"`
3. 将新的 FIT 文件放入 `data/` 目录（如 `data/2024_FIT/`）
4. 运行导入命令：`python data-manager/main.py import ./data/2024_FIT/`
5. 导出 JSON 数据：`python data-manager/main.py export`
6. 启动前端开发服务器：`cd frontend && npm run dev`

### 13.2 GitHub Actions 更新流程（待配置）
1. 将新的 FIT 文件提交到仓库的 `data/` 目录
2. GitHub Actions 工作流自动触发
3. 数据管理程序自动解析 FIT 文件并导入数据库
4. 自动导出 JSON 数据到 `frontend/public/data/data.json`
5. 自动提交并推送更新的数据文件

## 十四、扩展性设计

### 14.1 数据源扩展（未来可能）
- 支持直接读取 SQLite 数据库（sql.js）
- 支持多种数据源（CSV、GPX 等）
- 支持 API 数据源
- 支持手动数据录入界面

### 14.2 可视化扩展（未来可能）
- 支持更多图表类型（折线图、饼图、散点图等）
- 支持地图轨迹展示（Leaflet/Mapbox）
- 支持数据对比功能（多时段对比）
- 支持自定义仪表盘布局

### 14.3 功能扩展（未来可能）
- 地图页面（当前已预留导航入口）
- 支持多用户切换
- 支持数据分享（生成分享链接）
- 支持社交功能（评论、点赞）
- 支持数据导出为图片/PDF
- 支持目标设定和达成率追踪

## 十五、版本记录

- **v1.0** (2026-04-07): 初始版本，完整的技术规格说明
- **v1.1** (2026-04-08): 更新年份选择器设计、日历图高度自适应、表头优化、地图菜单
- **v1.2** (2026-04-08): 更新组件结构说明，整合用户信息到 Dashboard，简化路由配置
- **v2.0** (2026-04-08): 根据实际代码重构技术规格
  - 更新技术栈版本信息（Vue 3.5+, Vite 8, Pinia 3, TypeScript, Tailwind CSS 4）
  - 更新目录结构（反映实际文件组织）
  - 更新数据模型（增加 display_name 字段）
  - 完善 CLI 命令文档（新增 user delete, activity 命令组）
  - 详细描述所有前端组件的实现细节
  - 补充状态管理的完整 API 文档
  - 更新数据处理逻辑说明

---

**文档最后更新：** 2026-04-08
**文档维护者：** 项目开发团队
