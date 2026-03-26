# 运动数据仪表盘技术规格说明书

## 一、项目概述

### 1.1 项目目标
开发一个基于Vue3的运动数据展示网站，实现运动数据的可视化展示和管理。

### 1.2 技术栈
- 前端框架：Vue 3
- 构建工具：Vite
- 数据可视化：ECharts
- 后端：Python Flask
- 数据库：SQLite3
- FIT文件解析：fitparse库
- HTTP请求：requests库

## 二、系统架构

### 2.1 整体架构
```
┌─────────────────┐
│   前端 (Vue3)   │
│  - 数据展示     │
│  - 用户交互     │
└────────┬────────┘
         │ HTTP API
┌────────▼────────┐
│  后端 (Flask)   │
│  - 数据解析     │
│  - 数据管理     │
│  - API接口      │
└────────┬────────┘
         │
┌────────▼────────┐
│  数据库(SQLite) │
│  - 运动数据     │
│  - 用户信息     │
└─────────────────┘
```

### 2.2 目录结构
```
sports-data-dashboard/
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── views/         # 页面视图
│   │   ├── api/           # API调用
│   │   ├── stores/        # 状态管理
│   │   └── utils/         # 工具函数
│   ├── package.json
│   └── vite.config.js
├── backend/               # 后端项目
│   ├── app.py            # Flask应用主文件
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   │   ├── fit_parser.py # FIT文件解析
│   │   └── igsports.py   # iGSports数据获取
│   └── database.py       # 数据库配置
├── docs/                 # 文档
│   ├── requirements.md   # 需求规格说明书
│   ├── spec.md          # 技术规格说明书
│   ├── tasks.md         # 任务分解
│   └── checklist.md     # 完成清单
└── README.md
```

## 三、数据模型设计

### 3.1 用户信息表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    avatar_url VARCHAR(255),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 运动数据表 (activities)
```sql
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    duration INTEGER,  -- 秒
    distance REAL,      -- 米
    calories REAL,
    max_speed REAL,
    avg_speed REAL,
    max_heart_rate INTEGER,
    avg_heart_rate INTEGER,
    elevation_gain REAL,  -- 米
    data_source VARCHAR(50),  -- 'fit_file' 或 'igsports'
    raw_data TEXT,  -- JSON格式存储原始数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 3.3 数据库索引
```sql
CREATE INDEX idx_activities_user_id ON activities(user_id);
CREATE INDEX idx_activities_start_time ON activities(start_time);
CREATE INDEX idx_activities_year ON activities(strftime('%Y', start_time));
```

## 四、API接口设计

### 4.1 用户相关接口

#### 4.1.1 获取用户信息
```
GET /api/user/:userId
Response:
{
    "id": 1,
    "username": "user123",
    "avatar_url": "https://...",
    "bio": "运动爱好者",
    "stats": {
        "total_activities_last_year": 52,
        "total_distance_last_year": 520.5,
        "total_duration_last_year": 31200
    }
}
```

#### 4.1.2 更新用户信息
```
PUT /api/user/:userId
Request:
{
    "avatar_url": "https://...",
    "bio": "新的简介"
}
Response:
{
    "success": true,
    "message": "用户信息更新成功"
}
```

### 4.2 运动数据接口

#### 4.2.1 上传FIT文件
```
POST /api/activities/upload
Content-Type: multipart/form-data
Request:
{
    "file": <FIT file>,
    "user_id": 1
}
Response:
{
    "success": true,
    "activity_id": 123,
    "message": "文件解析成功"
}
```

#### 4.2.2 从iGSports获取数据
```
POST /api/activities/igsports
Request:
{
    "user_id": 1,
    "igsports_url": "https://..."
}
Response:
{
    "success": true,
    "imported_count": 5,
    "message": "成功导入5条运动数据"
}
```

#### 4.2.3 获取日历数据
```
GET /api/activities/calendar?userId=1&year=2024
Response:
{
    "year": 2024,
    "data": {
        "2024-01-15": {
            "count": 2,
            "distance": 15.5,
            "activities": [...]
        },
        ...
    }
}
```

#### 4.2.4 获取柱形图数据
```
GET /api/activities/chart?userId=1&mode=week
Response:
{
    "mode": "week",
    "labels": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    "data": {
        "count": [1, 0, 2, 1, 0, 3, 1],
        "distance": [10.5, 0, 21.3, 8.7, 0, 45.2, 12.1]
    }
}
```

#### 4.2.5 获取运动列表
```
GET /api/activities?userId=1&page=1&pageSize=20
Response:
{
    "total": 100,
    "page": 1,
    "page_size": 20,
    "data": [
        {
            "id": 1,
            "activity_type": "running",
            "start_time": "2024-01-15T08:00:00",
            "duration": 3600,
            "distance": 10500,
            "calories": 500,
            ...
        },
        ...
    ]
}
```

#### 4.2.6 删除运动数据
```
DELETE /api/activities/:activityId
Response:
{
    "success": true,
    "message": "删除成功"
}
```

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
- 显示最近1年运动统计（次数、距离、时长）
- 支持编辑用户信息

#### 5.2.2 CalendarView.vue
- 使用ECharts日历图展示运动数据
- 支持年份切换
- 鼠标悬停显示当日运动详情
- 颜色深浅表示运动强度

#### 5.2.3 ChartView.vue
- 使用ECharts柱形图展示运动数据
- 支持四种显示模式：周、月、年、全部
- 双Y轴：左侧显示运动次数，右侧显示运动距离
- 支持数据导出功能

#### 5.2.4 ActivityList.vue
- 表格展示运动数据列表
- 支持分页
- 支持删除操作
- 支持按日期、类型筛选

### 5.3 状态管理 (Pinia)

#### 5.3.1 userStore
```javascript
state: {
    currentUser: null,
    stats: null
}
actions: {
    fetchUser(userId),
    updateUser(data),
    fetchStats(userId)
}
```

#### 5.3.2 activityStore
```javascript
state: {
    activities: [],
    calendarData: {},
    chartData: {},
    currentMode: 'week',
    currentYear: new Date().getFullYear()
}
actions: {
    fetchActivities(params),
    fetchCalendarData(year),
    fetchChartData(mode),
    uploadFitFile(file),
    importFromIGSports(url),
    deleteActivity(id)
}
```

## 六、FIT文件解析规范

### 6.1 解析流程
1. 读取FIT文件
2. 验证文件格式
3. 提取运动类型、开始时间、持续时间
4. 提取距离、卡路里、速度等数据
5. 提取心率数据（如果有）
6. 提取海拔数据（如果有）
7. 保存到数据库

### 6.2 支持的运动类型
- running (跑步)
- cycling (骑行)
- swimming (游泳)
- walking (健走)
- hiking (徒步)
- other (其他)

### 6.3 数据映射
```python
FIT字段 -> 数据库字段
sport -> activity_type
timestamp -> start_time
total_timer_time -> duration
total_distance -> distance
total_calories -> calories
enhanced_max_speed -> max_speed
enhanced_avg_speed -> avg_speed
max_heart_rate -> max_heart_rate
avg_heart_rate -> avg_heart_rate
total_ascent -> elevation_gain
```

## 七、iGSports数据获取规范

### 7.1 数据获取流程
1. 解析用户提供的iGSports个人主页URL
2. 模拟浏览器访问获取HTML内容
3. 解析HTML提取运动数据列表
4. 逐条获取运动详情
5. 数据去重（根据开始时间判断）
6. 保存新数据到数据库

### 7.2 数据字段映射
```python
iGSports字段 -> 数据库字段
运动类型 -> activity_type
开始时间 -> start_time
时长 -> duration
距离 -> distance
消耗卡路里 -> calories
配速 -> avg_speed
最大配速 -> max_speed
最大心率 -> max_heart_rate
平均心率 -> avg_heart_rate
爬升海拔 -> elevation_gain
```

## 八、前端路由设计

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

## 九、部署方案

### 9.1 开发环境
- 前端：`npm run dev` (端口 5173)
- 后端：`python app.py` (端口 5000)
- 数据库：SQLite文件存储

### 9.2 生产环境
- 前端：构建静态文件，使用Nginx托管
- 后端：使用Gunicorn + Flask部署
- 数据库：SQLite文件存储（定期备份）

## 十、性能优化

### 10.1 前端优化
- 组件懒加载
- 虚拟滚动（长列表）
- 图表数据缓存
- 图片懒加载

### 10.2 后端优化
- 数据库查询优化（索引、分页）
- API响应缓存
- FIT文件异步解析
- 批量数据导入优化

## 十一、安全考虑

### 11.1 数据验证
- FIT文件格式验证
- API参数验证
- 文件上传大小限制

### 11.2 数据安全
- SQL注入防护（使用ORM）
- XSS防护（前端输入转义）
- CSRF防护（Token验证）

## 十二、测试策略

### 12.1 单元测试
- FIT文件解析逻辑测试
- 数据模型测试
- API接口测试

### 12.2 集成测试
- 前后端集成测试
- 数据导入流程测试

### 12.3 E2E测试
- 用户操作流程测试
- 数据可视化展示测试