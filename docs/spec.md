# 运动数据仪表盘技术规格说明书

## 一、项目概述

### 1.1 项目目标
开发一个基于Vue3的运动数据展示网站，实现运动数据的可视化展示。数据管理作为独立程序运行，可以在本地或GitHub Actions中执行。

### 1.2 技术栈
- 前端框架：Vue 3
- 构建工具：Vite
- 数据可视化：ECharts
- 数据管理程序：Python
- 数据库：SQLite3 或 JSON文件
- FIT文件解析：fitparse库

## 二、系统架构

### 2.1 整体架构
```
┌─────────────────────────────────────────┐
│         前端 (Vue3 静态网站)             │
│  - 数据展示 (直接读取数据文件)           │
│  - 用户交互                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      数据文件 (SQLite3 或 JSON)          │
│  - 运动数据                              │
│  - 用户信息                              │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    数据管理程序 (Python CLI 工具)       │
│  - FIT文件解析                          │
│  - 数据导入                              │
│  - 数据管理                              │
└─────────────────────────────────────────┘
```

### 2.2 目录结构
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
│   │       ├── data.json  # JSON数据文件 (可选)
│   │       └── data.db    # SQLite数据库文件 (可选)
│   ├── package.json
│   └── vite.config.js
├── data-manager/          # 数据管理程序
│   ├── main.py           # 主程序入口
│   ├── parser.py         # FIT文件解析器
│   ├── database.py       # 数据库操作
│   ├── exporter.py       # 数据导出
│   └── config.py         # 配置文件
├── docs/                 # 文档
│   ├── requirements.md   # 需求规格说明书
│   ├── spec.md          # 技术规格说明书
│   ├── tasks.md         # 任务分解
│   └── checklist.md     # 完成清单
└── README.md
```

## 三、数据模型设计

### 3.1 用户信息
```json
{
    "user": {
        "id": 1,
        "username": "user123",
        "avatar_url": "https://...",
        "bio": "运动爱好者"
    }
}
```

### 3.2 运动数据
```json
{
    "activities": [
        {
            "id": 1,
            "activity_type": "running",
            "start_time": "2024-01-15T08:00:00",
            "duration": 3600,
            "distance": 10500,
            "calories": 500,
            "max_speed": 4.5,
            "avg_speed": 2.9,
            "max_heart_rate": 180,
            "avg_heart_rate": 150,
            "max_cadence": 95,
            "avg_cadence": 85,
            "max_power": 350,
            "avg_power": 200,
            "normalized_power": 220,
            "elevation_gain": 120
        }
    ]
}
```

**注意：** 心率、踏频、功率等字段为可选字段，根据FIT文件中是否包含相应数据而定。如果FIT文件中没有这些数据，对应字段将为null或不存在。

### 3.3 SQLite表结构（可选）

#### 3.3.1 用户信息表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
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
    duration INTEGER,
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

**注意：** 心率、踏频、功率、海拔等字段允许为NULL，因为不是所有FIT文件都包含这些数据。

## 四、数据管理程序设计

### 4.1 程序架构
```
data-manager/
├── main.py              # CLI入口
├── parser.py            # FIT文件解析
├── database.py          # 数据库操作
├── exporter.py          # 数据导出
└── config.py            # 配置管理
```

### 4.2 CLI命令接口

#### 4.2.1 初始化数据库
```bash
python main.py init --output ./data/data.db
```

#### 4.2.2 导入FIT文件
```bash
python main.py import ./fit-files/ --output ./data/data.db
```

#### 4.2.3 导出为JSON
```bash
python main.py export --input ./data/data.db --output ./data/data.json
```

#### 4.2.4 查看统计信息
```bash
python main.py stats --input ./data/data.db
```

#### 4.2.5 用户管理
```bash
# 初始化用户信息
python main.py user init "username" --avatar "avatar_url" --bio "user bio"

# 查看用户信息
python main.py user show [username]

# 更新用户信息
python main.py user update "username" --avatar "new_avatar_url" --bio "new bio"
```

### 4.3 FIT文件解析规范

#### 4.3.1 解析流程
1. 读取FIT文件
2. 验证文件格式
3. 提取运动类型、开始时间、持续时间
4. 提取距离、卡路里、速度等数据
5. 提取心率数据（最大心率、平均心率）- 如果FIT文件包含心率数据
6. 提取踏频数据（最大踏频、平均踏频）- 如果FIT文件包含踏频数据
7. 提取功率数据（最大功率、平均功率、标准化功率）- 如果FIT文件包含功率数据
8. 提取海拔数据（爬升海拔）- 如果FIT文件包含海拔数据
9. 保存到数据库（不存在的数据字段设为NULL）

#### 4.3.2 支持的运动类型
- running (跑步)
- cycling (骑行)
- swimming (游泳)
- walking (健走)
- hiking (徒步)
- other (其他)

#### 4.3.3 数据映射
```python
FIT字段 -> 数据库字段
sport -> activity_type
start_time -> start_time
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

**注意：** 标记为"可选"的字段表示不是所有FIT文件都包含这些数据。如果FIT文件中没有对应数据，这些字段在数据库中将存储为NULL。

### 4.4 数据导出格式

#### 4.4.1 JSON格式
```json
{
    "user": {
        "id": 1,
        "username": "user123",
        "avatar_url": "https://...",
        "bio": "运动爱好者"
    },
    "activities": [
        {
            "id": 1,
            "activity_type": "running",
            "start_time": "2024-01-15T08:00:00",
            "duration": 3600,
            "distance": 10500,
            "calories": 500,
            "max_speed": 4.5,
            "avg_speed": 2.9,
            "max_heart_rate": 180,
            "avg_heart_rate": 150,
            "max_cadence": 95,
            "avg_cadence": 85,
            "max_power": 350,
            "avg_power": 200,
            "normalized_power": 220,
            "elevation_gain": 120
        }
    ]
}
```

**注意：** 心率、踏频、功率、海拔等字段为可选字段，根据FIT文件中是否包含相应数据而定。如果FIT文件中没有这些数据，对应字段将为null或从JSON中省略。

## 五、前端组件设计

### 5.1 页面结构
```
App.vue
├── Header.vue          # 顶部导航
├── UserProfile.vue     # 用户信息展示
├── Dashboard.vue       # 主仪表盘
│   ├── CalendarView.vue    # 日历视图
│   └── ChartView.vue       # 柱形图视图
└── ActivityList.vue   # 运动列表
```

### 5.2 核心组件

#### 5.2.1 UserProfile.vue
- 显示用户头像、用户名、简介
- 显示最近 1 周运动数据统计（总距离、总时长、总次数、总热量、平均速度）
- 从数据文件读取用户信息
- 显示本周日期范围标签 (MM/DD - MM/DD)

#### 5.2.2 CalendarView.vue
- 使用 ECharts 日历图展示运动数据
- 支持年份切换，默认展示数据中最新 1 年的运动数据
- 年份选择器：点击年份弹出弹窗式选择器，3 列网格布局，每页 12 个年份
  - 顶部导航：左右箭头翻页，显示年份范围
  - 年份单元格：悬停效果，当前选中蓝色高亮
  - 点击外部自动关闭
- 鼠标悬停显示当日运动详情
- 默认以距离着色，可切换为时长、次数、热量、平均速度着色
- 颜色深浅表示运动强度
- 今天标记：红色背景突出显示今天的单元格，Tooltip 显示"(今天)"标记
- 图注：显示无数据、低、中、高、极高、今天
- 指标选择器：垂直排列在日历图左侧，图标 + 文字
- 卡片高度：100%，与左侧周统计卡片高度相等
- 图表区域：自适应填充剩余空间

#### 5.2.3 ChartView.vue
- 使用 ECharts 柱形图展示运动数据
- 支持四种显示模式：周、月、年、全部
- 数据统计部分按对应周期统计：总距离、总时长、总次数、总热量、平均速度
- 柱形图纵轴默认为运动距离，可切换为时长、次数、热量、平均速度
- 柱形图横轴配置：
  - 周模式：横轴为天
  - 月模式：横轴为天
  - 年模式：横轴为周
  - 全部模式：横轴为年
- 翻页组件：只显示当前日期范围，不支持用户输入
  - 周模式：显示周范围 (MM/DD - MM/DD)，周一作为一周起始
  - 月模式：显示月份 (YYYY/MM)
  - 年模式：显示年份 (YYYY 年)
  - 全部模式：显示运动生涯 (YYYY - YYYY)
- 数据格式：
  - 次数显示为整数
  - 其他指标保留一位小数
- Y 轴名称加粗显示，颜色更深

#### 5.2.4 ActivityList.vue
- 表格展示运动数据列表
- 显示字段：运动日期、运动类型（中文）、运动距离、运动时长、热量 (kcal)、平均速度、最大速度、平均心率、最大心率、平均踏频、最大踏频
- 支持分页
- 支持按日期、类型筛选
- 默认以运动日期倒序排列，支持点击表头切换排序方式
- 运动类型映射：cycling/riding→骑行，running→跑步，swimming→游泳，walking→健走，hiking→徒步

### 5.3 数据读取层

#### 5.3.1 SQLite数据读取
```javascript
// utils/sqlite-reader.js
import initSqlJs from 'sql.js';

async function loadDatabase() {
    const SQL = await initSqlJs();
    const response = await fetch('/data/data.db');
    const arrayBuffer = await response.arrayBuffer();
    const db = new SQL.Database(new Uint8Array(arrayBuffer));
    return db;
}

export async function getActivities() {
    const db = await loadDatabase();
    const result = db.exec('SELECT * FROM activities ORDER BY start_time DESC');
    return result[0].values.map(row => ({
        id: row[0],
        activity_type: row[1],
        start_time: row[2],
        duration: row[3],
        distance: row[4],
        calories: row[5],
        max_speed: row[6],
        avg_speed: row[7],
        max_heart_rate: row[8],     // 可能为null
        avg_heart_rate: row[9],     // 可能为null
        max_cadence: row[10],       // 可能为null
        avg_cadence: row[11],       // 可能为null
        max_power: row[12],         // 可能为null
        avg_power: row[13],         // 可能为null
        normalized_power: row[14],  // 可能为null
        elevation_gain: row[15]     // 可能为null
    }));
}
```

#### 5.3.2 JSON数据读取
```javascript
// utils/json-reader.js
export async function loadData() {
    const response = await fetch('/data/data.json');
    const data = await response.json();
    return data;
}

export async function getActivities() {
    const data = await loadData();
    return data.activities;
}
```

### 5.4 状态管理 (Pinia)

#### 5.4.1 dataStore
```javascript
state: {
    user: null,
    activities: [],
    calendarData: {},
    chartData: {},
    weekStats: {},           // 最近 1 周统计数据
    currentMode: 'week',     // 当前显示模式：week/month/year/all
    currentYear: new Date().getFullYear(),
    calendarMetric: 'distance',  // 日历图着色指标
    chartMetric: 'distance'      // 柱形图纵轴指标
}
actions: {
    loadData(),
    processCalendarData(year, metric),
    processChartData(mode, metric),
    getWeekStats(),           // 获取最近 1 周运动统计
    setYear(year),            // 设置当前年份
    setCalendarMetric(metric), // 设置日历图指标
    setChartMetric(metric)    // 设置柱形图指标
}
```

### 5.5 页面设计

#### 5.5.1 仪表盘页 (Dashboard)
上下两栏结构，顶部为导航区，底部为内容区。

**导航区：**
- 左侧：个人信息展示（头像、用户名、简介）
- 右侧：导航菜单（仪表盘、运动记录、地图）
- 地图菜单：点击提示"地图页面正在开发中，敬请期待！"

**内容区 - 上半部分：**
- 左侧 1/4 区域：最近 1 周运动数据统计
- 右侧 3/4 区域：日历图
- 高度：左右两侧卡片高度相等（100%）

**内容区 - 下半部分：**
- 柱形图
- 高度自适应

#### 5.5.2 运动记录页 (ActivityList)
上下两栏结构，顶部为导航区，底部为内容区。

**导航区：** 与仪表盘页面相同

**内容区：** 运动数据表格

## 六、前端路由设计

```javascript
const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/activities',
        name: 'ActivityList',
        component: ActivityList
    },
    {
        path: '/profile',
        name: 'Profile',
        component: UserProfile
    }
]
```

## 七、GitHub Actions集成

### 7.1 自动化工作流
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
          python data-manager/main.py import ./fit-files/ --output ./frontend/public/data/data.db
      - name: Export to JSON
        run: |
          python data-manager/main.py export --input ./frontend/public/data/data.db --output ./frontend/public/data/data.json
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
- 前端：`npm run dev` (端口 5173)
- 数据管理：`python data-manager/main.py import ./fit-files/`
- 数据文件：SQLite或JSON存储在`frontend/public/data/`目录

### 8.2 生产环境
- 前端：构建静态文件，使用GitHub Pages或Netlify托管
- 数据管理：在本地或GitHub Actions中运行
- 数据文件：随静态文件一起部署

## 九、性能优化

### 9.1 前端优化
- 组件懒加载
- 虚拟滚动（长列表）
- 图表数据缓存
- 数据文件压缩

### 9.2 数据管理优化
- 批量导入FIT文件
- 数据去重优化
- 增量更新支持

## 十、安全考虑

### 10.1 数据验证
- FIT文件格式验证
- 数据完整性检查
- 文件大小限制

### 10.2 数据安全
- 数据文件版本控制
- 敏感信息过滤
- 数据备份机制

## 十一、测试策略

### 11.1 单元测试
- FIT文件解析逻辑测试
- 数据导出逻辑测试
- 数据处理逻辑测试

### 11.2 集成测试
- 数据导入导出流程测试
- 前端数据读取测试

### 11.3 E2E测试
- 用户操作流程测试
- 数据可视化展示测试

## 十二、配置管理

### 12.1 数据管理程序配置
```python
# config.py
DATA_DIR = "./data"
OUTPUT_DIR = "./frontend/public/data"
DATABASE_FILE = "data.db"
JSON_FILE = "data.json"
SUPPORTED_TYPES = ["running", "cycling", "swimming", "walking", "hiking", "other"]
```

### 12.2 前端配置
```javascript
// config.js
export const config = {
    dataSource: 'json', // 'json' 或 'sqlite'
    dataPath: '/data/data.json',
    defaultYear: new Date().getFullYear(),
    defaultMode: 'week'
};
```

## 十三、数据更新流程

### 13.1 本地更新流程
1. 初始化数据库：`python data-manager/main.py init`
2. 初始化用户信息：`python data-manager/main.py user init "username" --avatar "avatar_url" --bio "user bio"`
3. 将新的FIT文件放入`fit-files/`目录
4. 运行数据管理程序：`python data-manager/main.py import ./fit-files/`
5. 导出数据：`python data-manager/main.py export`
6. 启动前端开发服务器：`npm run dev`

### 13.2 GitHub Actions更新流程
1. 将新的FIT文件提交到仓库
2. GitHub Actions自动触发工作流
3. 数据管理程序自动解析FIT文件
4. 自动导出JSON数据
5. 自动提交并推送更新

## 十四、扩展性设计

### 14.1 数据源扩展
- 支持多种数据源（CSV、GPX等）
- 支持API数据源
- 支持手动数据录入

### 14.2 可视化扩展
- 支持更多图表类型（折线图、饼图等）
- 支持地图轨迹展示
- 支持数据对比功能

### 14.3 功能扩展
- 支持多用户
- 支持数据分享
- 支持社交功能

## 十五、版本记录

- v1.0 (2026-04-07): 初始版本，完整的技术规格说明
- v1.1 (2026-04-08): 更新年份选择器、日历图高度自适应、表头优化、地图菜单等

---

**文档结束**