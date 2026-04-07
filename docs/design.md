# 运动数据仪表盘 - 高保真设计文档

## 一、设计概览

本文档定义了运动数据仪表盘网站的完整视觉设计规范，包括配色方案、组件设计、交互细节和响应式布局。

---

## 二、配色方案

### 2.1 品牌色

```
主色：
- Primary: #8B5CF6 (紫色)
- Primary Light: #A78BFA
- Primary Dark: #7C3AED

强调色：
- Accent: #F97316 (橙色)
- Accent Light: #FB923C
- Accent Dark: #EA580C

渐变：
- Primary Gradient: linear-gradient(135deg, #8B5CF6 0%, #F97316 100%)
- Secondary Gradient: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)
```

### 2.2 功能色

```
成功：#10B981 (绿色)
警告：#F59E0B (黄色)
错误：#EF4444 (红色)
信息：#3B82F6 (蓝色)
```

### 2.3 中性色

```
文本：
- Text Primary: #1F2937
- Text Secondary: #6B7280
- Text Disabled: #9CA3AF

背景：
- Background: #F9FAFB
- Surface: #FFFFFF
- Border: #E5E7EB

叠加：
- Overlay: rgba(0, 0, 0, 0.5)
```

### 2.4 数据可视化配色

```
图表色系（5 级）：
Level 1: #DBEAFE (浅蓝)
Level 2: #93C5FD (中蓝)
Level 3: #3B82F6 (深蓝)
Level 4: #2563EB (藏蓝)
Level 5: #1E40AF (深蓝紫)

热力图色系（5 级）：
Level 1: #FEF3C7 (浅黄)
Level 2: #FDE68A (中黄)
Level 3: #FBBF24 (深黄)
Level 4: #F59E0B (橙黄)
Level 5: #EF4444 (橙红)

运动类型配色：
- Riding: #8B5CF6 (紫色)
- Running: #F97316 (橙色)
- Swimming: #3B82F6 (蓝色)
- Walking: #10B981 (绿色)
- Hiking: #84CC16 (黄绿)
```

---

## 三、设计令牌

### 3.1 间距系统

```
基于 4px 网格：
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px
```

### 3.2 圆角

```
- none: 0
- sm: 4px
- md: 8px
- lg: 12px
- xl: 16px
- 2xl: 24px
- full: 9999px
```

### 3.3 阴影

```
- sm: 0 1px 2px rgba(0, 0, 0, 0.05)
- md: 0 4px 6px rgba(0, 0, 0, 0.1)
- lg: 0 10px 15px rgba(0, 0, 0, 0.1)
- xl: 0 20px 25px rgba(0, 0, 0, 0.15)
- 2xl: 0 25px 50px rgba(0, 0, 0, 0.25)
```

### 3.4 字体

```
字体系列：
- Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Mono: 'Fira Code', monospace

字号：
- xs: 12px
- sm: 14px
- base: 16px
- lg: 18px
- xl: 20px
- 2xl: 24px
- 3xl: 30px
- 4xl: 36px

字重：
- light: 300
- regular: 400
- medium: 500
- semibold: 600
- bold: 700
```

---

## 四、核心组件设计

### 4.1 导航栏

**规格：**
```
高度：80px
背景：linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)
阴影：0 4px 6px rgba(0, 0, 0, 0.1)
```

**左侧用户信息区：**
```
布局：flex row, align-items: center
头像：48px × 48px, border-radius: 50%
用户名：16px, 600, #FFFFFF
简介：14px, 400, rgba(255, 255, 255, 0.8)
间距：头像与文字间距 12px
```

**右侧导航菜单：**
```
菜单项：
- 默认状态：文字 15px, 500, rgba(255, 255, 255, 0.8)
- Hover 状态：文字 #FFFFFF, 背景 rgba(255, 255, 255, 0.1)
- 激活状态：文字 #FFFFFF, 背景 rgba(255, 255, 255, 0.2), border-bottom: 2px solid #FFFFFF
- 禁用状态：文字 rgba(255, 255, 255, 0.4)

间距：菜单项之间 32px
内边距：左右各 40px
```

### 4.2 统计卡片

**规格：**
```
尺寸：宽度 200px, 高度 120px
背景：#FFFFFF
圆角：16px
阴影：0 4px 6px rgba(0, 0, 0, 0.05)
边框：1px solid #E5E7EB
内边距：20px
```

**内容布局：**
```
图标区：
- 尺寸：40px × 40px
- 圆角：12px
- 背景：渐变色（根据指标类型）
- 图标：24px, #FFFFFF

指标名称：
- 字号：14px
- 字重：500
- 颜色：#6B7280
- 间距：8px

指标值：
- 字号：28px
- 字重：700
- 颜色：#1F2937
- 字体：Inter

趋势指示器：
- 上升：12px, #10B981, ↑
- 下降：12px, #EF4444, ↓
- 持平：12px, #9CA3AF, →
```

**5 个指标卡片配色：**
```
总距离：gradient(#3B82F6, #2563EB)
总时长：gradient(#F97316, #EA580C)
总次数：gradient(#8B5CF6, #7C3AED)
总热量：gradient(#EF4444, #DC2626)
平均速度：gradient(#10B981, #059669)
```

**交互状态：**
```
Hover:
- 阴影：0 10px 15px rgba(0, 0, 0, 0.1)
- 位移：translateY(-4px)
- 过渡：all 0.3s ease

Active:
- 阴影：0 4px 6px rgba(0, 0, 0, 0.05)
- 位移：translateY(0)
```

### 4.3 日历热力图

**规格：**
```
容器：
- 背景：#FFFFFF
- 圆角：16px
- 阴影：0 4px 6px rgba(0, 0, 0, 0.05)
- 内边距：24px

网格：
- 列数：53 周
- 行数：7 天
- 单元格：12px × 12px
- 间距：4px
- 圆角：2px
```

**热力图颜色强度：**
```
Level 0 (无数据): #F3F4F6
Level 1 (低): #DBEAFE
Level 2 (中低): #93C5FD
Level 3 (中): #3B82F6
Level 4 (高): #2563EB
Level 5 (极高): #1E40AF

今天标记：红色背景 (#EF4444) 突出显示今天的单元格，Tooltip 显示"(今天)"标记
```

**图例：**
```
位置：底部居中
布局：flex row
标签：12px, #6B7280
色块：12px × 12px, 间距 4px
显示：无数据、低、中低、中、高、极高、今天
```

**年份切换器：**
```
位置：右上角
样式：点击年份弹出年份选择器
字号：14px
颜色：#1F2937
边框：1px solid #E5E7EB
圆角：6px
内边距：0 12px
光标：pointer

年份选择器弹窗:
- 位置：年份输入框下方
- 背景：#FFFFFF
- 圆角：8px
- 阴影：0 4px 20px rgba(0, 0, 0, 0.15)
- 边框：1px solid #E5E7EB
- 内边距：12px
- 最小宽度：220px
- 布局：3 列网格，每页 12 个年份，支持翻页浏览
- 顶部导航：左右箭头翻页，显示年份范围
- 年份单元格：
  - 内边距：8px 12px
  - 圆角：6px
  - 字号：13px
  - 悬停背景：#F3F4F6
  - 当前选中：背景 #3B82F6, 文字 #FFFFFF
```

**指标切换按钮组：**
```
位置：年份切换器左侧
布局：垂直排列在日历图左侧
按钮：
- 默认：文字 13px, #6B7280, 图标 + 文字
- 激活：文字 #FFFFFF, 背景 #8B5CF6
- Hover：背景 #F3F4F6
圆角：6px
间距：8px
内边距：12px 16px
```

**交互：**
```
单元格 Hover:
- 显示 Tooltip
- 放大：scale(1.2)
- 阴影：0 2px 4px rgba(0, 0, 0, 0.1)
- 过渡：all 0.2s ease

Tooltip:
- 背景：#1F2937
- 文字：#FFFFFF
- 圆角：8px
- 内边距：8px 12px
- 字号：12px
- 阴影：0 4px 6px rgba(0, 0, 0, 0.1)
```

### 4.4 柱形图

**规格：**
```
容器：
- 背景：#FFFFFF
- 圆角：16px
- 阴影：0 4px 6px rgba(0, 0, 0, 0.05)
- 内边距：24px

图表区域：
- 高度：300px
- 背景：#F9FAFB
- 边框：1px solid #E5E7EB
- 圆角：8px
```

**柱形样式：**
```
默认柱形：
- 宽度：根据数据量动态计算
- 圆角：4px 4px 0 0
- 渐变：linear-gradient(180deg, #8B5CF6 0%, #6366F1 100%)
- 背景：rgba(139, 92, 246, 0.1)

Hover 状态：
- 亮度：+10%
- 显示 Tooltip
- 过渡：all 0.2s ease
```

**坐标轴：**
```
X 轴：
- 线宽：1px
- 颜色：#E5E7EB
- 标签：12px, #6B7280

Y 轴：
- 线宽：1px
- 颜色：#E5E7EB
- 标签：12px, #6B7280
- 网格线：1px dashed #E5E7EB
- 轴名称：13px, 加粗，#374151
```

**图例和切换器：**
```
位置：顶部右侧
按钮样式：同日历图指标切换器

翻页组件:
- 布局：按钮 + 标签 + 按钮
- 按钮：32px × 32px, 圆角 6px
- 标签：14px, 600, #1F2937
- 周模式：显示周范围 (MM/DD - MM/DD)
- 月模式：显示月份 (YYYY/MM)
- 年模式：显示年份 (YYYY 年)
- 全部模式：显示运动生涯 (YYYY - YYYY)
- 只显示当前日期范围，不支持用户输入

数据格式：
- 次数显示为整数
- 其他指标保留一位小数
```

### 4.5 数据表格

**规格：**
```
容器：
- 背景：#FFFFFF
- 圆角：16px
- 阴影：0 4px 6px rgba(0, 0, 0, 0.05)

表头：
- 高度：56px
- 背景：#F9FAFB
- 边框底部：1px solid #E5E7EB
- 文字：14px, 600, #6B7280

行：
- 高度：64px
- 边框底部：1px solid #F3F4F6
- 文字：14px, 400, #1F2937
- Hover 背景：#F9FAFB
- 选中背景：#F3F4F6
```

**列定义（11 列）：**
```
1. 复选框：40px
2. 运动日期：140px
3. 运动类型：100px (显示中文，如"骑行"、"跑步"等)
4. 运动距离：100px
5. 运动时长：100px
6. 热量：100px (带单位 kcal)
7. 平均速度：100px
8. 最大速度：100px
9. 平均心率：100px
10. 最大心率：100px
11. 平均踏频：100px
12. 最大踏频：100px
```

**排序指示器：**
```
位置：表头文字右侧
图标：8px × 8px
颜色：#9CA3AF
激活：#8B5CF6
```

**分页器：**
```
位置：表格底部右侧
布局：flex row, align-items: center
页码：
- 默认：32px × 32px, 文字 14px, #6B7280
- 激活：背景 #8B5CF6, 文字 #FFFFFF, 圆角 6px
- Hover：背景 #F3F4F6
间距：4px

信息显示：
- 位置：左侧
- 文字：14px, #6B7280
- 格式："显示 X-Y 条，共 Z 条"
```

**批量操作栏：**
```
显示条件：选中至少一行时
位置：表格顶部
背景：#EFF6FF
边框：1px solid #BFDBFE
圆角：8px
内边距：12px 16px

操作按钮：
- 批量删除：文字 14px, #EF4444, 图标左侧
- 取消选择：文字 14px, #6B7280
```

### 4.6 按钮

**主按钮：**
```
背景：linear-gradient(135deg, #8B5CF6 0%, #F97316 100%)
文字：#FFFFFF, 14px, 600
圆角：8px
内边距：10px 20px
阴影：0 2px 4px rgba(139, 92, 246, 0.3)

Hover:
- 阴影：0 4px 8px rgba(139, 92, 246, 0.4)
- 位移：translateY(-2px)

Active:
- 位移：translateY(0)
- 阴影：0 2px 4px rgba(139, 92, 246, 0.3)

Disabled:
- 背景：#D1D5DB
- 阴影：none
```

**次要按钮：**
```
背景：#FFFFFF
文字：#6B7280, 14px, 600
边框：1px solid #E5E7EB
圆角：8px
内边距：10px 20px

Hover:
- 背景：#F9FAFB
- 边框：#D1D5DB
```

**危险按钮：**
```
背景：#EF4444
文字：#FFFFFF, 14px, 600
圆角：8px
内边距：10px 20px

Hover:
- 背景：#DC2626
```

### 4.7 图标

```
尺寸系统：
- xs: 16px
- sm: 20px
- md: 24px
- lg: 32px
- xl: 48px

风格：
- 线性图标，2px 描边
- 圆角端点
- 填充图标用于特殊状态

颜色：
- 默认：#6B7280
- 主色：#8B5CF6
- 成功：#10B981
- 警告：#F59E0B
- 错误：#EF4444
```

---

## 五、页面布局

### 5.1 仪表盘页面

**整体结构：**
```
总宽度：100%
最小高度：calc(100vh - 80px)
背景：#F9FAFB
内边距：32px
```

**上部分区域：**
```
布局：flex row
间距：24px
高度：自动，由内容决定

左侧（1/4 宽度）：
- 周统计卡片组
- 垂直排列 5 个统计卡片
- 卡片高度 100%，与右侧日历图高度相等

右侧（3/4 宽度）：
- 日历热力图
- 包含标题、指标选择器、年份选择器、图例
- 卡片高度 100%，与左侧周统计高度相等
- 图表区域自适应填充剩余空间
```

**下部分区域：**
```
布局：vertical
间距：24px

下部：柱形图
- 全宽显示
- 高度自适应
- 包含指标选择器、翻页组件、图表、图例
```

### 5.2 运动记录页面

**整体结构：**
```
同仪表盘页面
```

**内容区：**
```
表格容器：
- 全宽显示
- 高度：auto（根据数据量）
- 包含分页器

筛选工具栏（可选）：
- 位置：表格上方
- 高度：56px
- 背景：#FFFFFF
- 圆角：16px
- 内边距：16px 24px

筛选器：
- 运动类型下拉框
- 日期范围选择器
- 搜索框
- 间距：16px
```

---

## 六、响应式设计

### 6.1 断点定义

```
手机：max-width: 639px
平板：min-width: 640px and max-width: 767px
小屏桌面：min-width: 768px and max-width: 1023px
中屏桌面：min-width: 1024px and max-width: 1279px
大屏桌面：min-width: 1280px
```

### 6.2 各断点适配

**手机 (<640px)：**
```
导航栏：
- 用户信息：只显示头像
- 菜单：汉堡菜单

统计卡片：
- 宽度：100%
- 布局：垂直堆叠

日历图：
- 单元格：8px × 8px
- 隐藏图例文字

表格：
- 横向滚动
- 显示关键列（日期、类型、距离、时长）
```

**平板 (640px-767px)：**
```
导航栏：
- 用户信息：头像 + 用户名

统计卡片：
- 2 列网格

日历图：
- 单元格：10px × 10px

表格：
- 显示主要列
```

**小屏桌面 (768px-1023px)：**
```
统计卡片：
- 3 列网格

日历图：
- 单元格：12px × 12px

表格：
- 显示所有列
```

**中屏桌面及以上 (≥1024px)：**
```
完整布局
```

---

## 七、交互动画

### 7.1 过渡时间

```
快速：150ms
正常：250ms
慢速：500ms
```

### 7.2 缓动函数

```
默认：cubic-bezier(0.4, 0, 0.2, 1)
进入：cubic-bezier(0, 0, 0.2, 1)
离开：cubic-bezier(0.4, 0, 1, 1)
弹性：cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

### 7.3 动画定义

```
页面进入：
- 透明度：0 → 1
- 位移：translateY(20px) → translateY(0)
- 时间：300ms

卡片 Hover：
- 位移：translateY(-4px)
- 阴影增强
- 时间：200ms

按钮点击：
- 缩放：scale(0.98)
- 时间：100ms

数据加载：
- 骨架屏闪烁
- 时间：1.5s 循环

图表加载：
- 柱形从下向上生长
- 时间：500ms
- 延迟：每根柱子 50ms
```

---

## 八、无障碍设计

### 8.1 对比度要求

```
普通文字：至少 4.5:1
大文字（18px+）：至少 3:1
UI 组件：至少 3:1
```

### 8.2 键盘导航

```
Tab 顺序：逻辑顺序
焦点样式：
- 外发光：2px solid #8B5CF6
- 外间距：2px
Enter/Space: 触发点击
Escape: 关闭弹窗
```

### 8.3 屏幕阅读器支持

```
所有图标按钮：aria-label
数据表格：aria-describedby 说明
图表：aria-label 数据摘要
状态变化：aria-live 区域
```

---

## 九、设计资源

### 9.1 推荐字体

```
Inter (Google Fonts)
Fira Code (代码/数字)
```

### 9.2 图标库

```
Heroicons (主要)
Phosphor Icons (补充)
```

### 9.3 图表库

```
ECharts 5.x
```

### 9.4 设计工具

```
Figma (设计稿)
Storybook (组件文档)
```

---

## 十、实施建议

### 10.1 Vue3 组件结构

```
components/
├── common/
│   ├── AppHeader.vue (导航栏)
│   ├── StatCard.vue (统计卡片)
│   ├── AppButton.vue (按钮)
│   └── AppTable.vue (表格)
├── dashboard/
│   ├── WeeklyStats.vue (周统计)
│   ├── CalendarHeatmap.vue (日历图)
│   └── StatsChart.vue (柱形图)
└── activities/
    └── ActivityTable.vue (运动表格)
```

### 10.2 CSS 架构

```
推荐使用：
- Tailwind CSS (实用优先)
- 或 SCSS + CSS Variables (设计令牌)

设计令牌变量：
:root {
  --color-primary: #8B5CF6;
  --color-accent: #F97316;
  --spacing-md: 16px;
  --radius-lg: 12px;
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

### 10.3 开发优先级

```
P0 - 核心组件：
1. 导航栏
2. 统计卡片
3. 数据表格
4. 按钮

P1 - 图表组件：
1. 日历热力图
2. 柱形图

P2 - 增强功能：
1. 响应式适配
2. 交互动画
3. 无障碍优化
```

---

## 十一、版本记录

- v1.0 (2026-04-07): 初始版本，完整的高保真设计规范
- v1.1 (2026-04-08): 更新年份选择器设计、日历图高度自适应、运动记录表头优化、地图菜单

---

**文档结束**
