<template>
  <AppCard class="chart-view" padding="none">
    <!-- 卡片标题区域 -->
    <div class="chart-header-section">
      <h3 class="chart-title">运动统计</h3>
      <div class="mode-selector-wrapper">
        <div class="mode-selector">
          <button
            v-for="m in modes"
            :key="m.value"
            :class="['mode-btn', { active: currentMode === m.value }]"
            @click="handleModeChange(m.value)"
          >
            {{ m.label }}
          </button>
        </div>
        <!-- 周模式：显示周范围 + 翻页 -->
        <div v-if="currentMode === 'week'" class="period-selector">
          <button class="period-btn" @click="previousPeriod" :disabled="!canPreviousPeriod">
            <span class="arrow">‹</span>
          </button>
          <span class="period-label">{{ weekRangeLabel }}</span>
          <button class="period-btn" @click="nextPeriod" :disabled="!canNextPeriod">
            <span class="arrow">›</span>
          </button>
        </div>
        <!-- 月模式：显示月份 + 翻页 -->
        <div v-else-if="currentMode === 'month'" class="period-selector">
          <button class="period-btn" @click="previousPeriod" :disabled="!canPreviousPeriod">
            <span class="arrow">‹</span>
          </button>
          <span class="period-label">{{ monthLabel }}</span>
          <button class="period-btn" @click="nextPeriod" :disabled="!canNextPeriod">
            <span class="arrow">›</span>
          </button>
        </div>
        <!-- 年模式：显示年份 + 翻页 -->
        <div v-else-if="currentMode === 'year'" class="period-selector">
          <button class="period-btn" @click="previousPeriod" :disabled="!canPreviousPeriod">
            <span class="arrow">‹</span>
          </button>
          <span class="period-label">{{ inputYear }}年</span>
          <button class="period-btn" @click="nextPeriod" :disabled="!canNextPeriod">
            <span class="arrow">›</span>
          </button>
        </div>
        <!-- 全部模式：显示运动生涯 -->
        <div v-else-if="currentMode === 'all'" class="period-selector">
          <span class="period-label">{{ careerLabel }}</span>
        </div>
      </div>
    </div>

    <!-- 卡片内容区域 -->
    <div class="chart-body">
      <!-- 左侧：统计卡片 -->
      <div class="stats-column">
        <StatsPanel
          :title="statsTitle"
          :stats="displayStats"
          variant="default"
        />
      </div>
      
      <!-- 中间：指标选择器 -->
      <MetricSelector
        v-model="currentMetric"
        :items="metricItems"
        @update:modelValue="handleMetricChange"
      />
      
      <!-- 右侧：柱形图 -->
      <div class="chart-column">
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import AppCard from '@/components/common/AppCard.vue'
import StatCard from '@/components/common/StatCard.vue'
import StatsPanel from '@/components/common/StatsPanel.vue'
import MetricSelector from '@/components/common/MetricSelector.vue'
import { useDataStore, type DisplayMode, type ChartMetric } from '@/stores/dataStore'

const dataStore = useDataStore()
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const currentMode = ref<DisplayMode>('week')
const currentMetric = ref<ChartMetric>('distance')
const currentWeekOffset = ref<number>(0)
const currentMonthOffset = ref<number>(0)

const modes = [
  { label: '周', value: 'week' as DisplayMode },
  { label: '月', value: 'month' as DisplayMode },
  { label: '年', value: 'year' as DisplayMode },
  { label: '全部', value: 'all' as DisplayMode }
]

const metrics = [
  { label: '距离', value: 'distance' as ChartMetric },
  { label: '时长', value: 'duration' as ChartMetric },
  { label: '次数', value: 'count' as ChartMetric },
  { label: '热量', value: 'calories' as ChartMetric },
  { label: '均速', value: 'avg_speed' as ChartMetric }
]

// 指标选项（带图标）
const metricItems = computed(() => metrics.map(m => ({
  ...m,
  icon: getMetricIcon(m.value)
})))

// 获取指标图标
const getMetricIcon = (metric: ChartMetric): string => {
  const iconMap: Record<ChartMetric, string> = {
    distance: '📍',
    duration: '⏱️',
    count: '🎯',
    calories: '🔥',
    avg_speed: '⚡'
  }
  return iconMap[metric] || '📊'
}

// 年份范围
const minYear = computed(() => {
  const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
  return years.length > 0 ? Math.min(...years) : new Date().getFullYear() - 1
})

const maxYear = computed(() => {
  const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
  return years.length > 0 ? Math.max(...years) : new Date().getFullYear()
})

// 图表标题
const chartTitle = computed(() => {
  const titleMap: Record<DisplayMode, string> = {
    week: '周统计',
    month: '月统计',
    year: '年统计',
    all: '运动生涯'
  }
  return titleMap[currentMode.value]
})

// 左侧统计标题
const statsTitle = computed(() => {
  const titleMap: Record<DisplayMode, string> = {
    week: '周统计',
    month: '月统计',
    year: '年统计',
    all: '运动生涯'
  }
  return titleMap[currentMode.value]
})

// 年份标签
const inputYear = computed(() => {
  return dataStore.currentYear
})

// 周范围标签
const weekRangeLabel = computed(() => {
  const now = new Date()
  const targetDate = new Date(now.getTime() - currentWeekOffset.value * 7 * 24 * 60 * 60 * 1000)
  // 周一作为一周的开始
  const day = targetDate.getDay()
  const diff = day === 0 ? 6 : day - 1
  const startOfWeek = new Date(targetDate)
  startOfWeek.setDate(targetDate.getDate() - diff)
  startOfWeek.setHours(0, 0, 0, 0)
  const endOfWeek = new Date(startOfWeek)
  endOfWeek.setDate(startOfWeek.getDate() + 6)
  endOfWeek.setHours(23, 59, 59, 999)
  
  const format = (date: Date) => {
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${month}/${day}`
  }
  
  return `${format(startOfWeek)} - ${format(endOfWeek)}`
})

// 月份标签
const monthLabel = computed(() => {
  const now = new Date()
  const targetMonth = new Date(now.getFullYear(), now.getMonth() - currentMonthOffset.value, 1)
  const year = targetMonth.getFullYear()
  const month = String(targetMonth.getMonth() + 1).padStart(2, '0')
  return `${year}/${month}`
})

// 运动生涯标签
const careerLabel = computed(() => {
  if (dataStore.activities.length === 0) return '无数据'
  const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
  const min = Math.min(...years)
  const max = Math.max(...years)
  return `${min} - ${max}`
})

// 是否可以翻页
const canPreviousPeriod = computed(() => {
  if (currentMode.value === 'week') {
    const now = new Date()
    const targetDate = new Date(now.getTime() - (currentWeekOffset.value + 1) * 7 * 24 * 60 * 60 * 1000)
    const minDate = new Date(minYear.value, 0, 1)
    return targetDate >= minDate
  } else if (currentMode.value === 'month') {
    const now = new Date()
    const targetMonth = new Date(now.getFullYear(), now.getMonth() - (currentMonthOffset.value + 1), 1)
    const minDate = new Date(minYear.value, 0, 1)
    return targetMonth >= minDate
  } else if (currentMode.value === 'year') {
    return inputYear.value > minYear.value
  }
  return false
})

const canNextPeriod = computed(() => {
  if (currentMode.value === 'week') {
    return currentWeekOffset.value > 0
  } else if (currentMode.value === 'month') {
    return currentMonthOffset.value > 0
  } else if (currentMode.value === 'year') {
    return inputYear.value < maxYear.value
  }
  return false
})

// 格式化统计数据
const displayStats = computed(() => {
  const { data } = dataStore.processChartData(currentMode.value, currentMetric.value)
  
  // 从原始活动数据中计算所有维度的总和
  const now = new Date()
  let filteredActivities = [...dataStore.activities]
  
  // 根据模式过滤数据 - 使用 dataStore 中的偏移量
  if (currentMode.value === 'week') {
    const targetDate = new Date(now.getTime() - dataStore.currentWeekOffset * 7 * 24 * 60 * 60 * 1000)
    const startOfWeek = new Date(targetDate)
    startOfWeek.setDate(targetDate.getDate() - targetDate.getDay())
    startOfWeek.setHours(0, 0, 0, 0)
    const endOfWeek = new Date(startOfWeek)
    endOfWeek.setDate(startOfWeek.getDate() + 6)
    endOfWeek.setHours(23, 59, 59, 999)
    
    filteredActivities = dataStore.activities.filter(a => {
      const activityDate = new Date(a.start_time)
      return activityDate >= startOfWeek && activityDate <= endOfWeek
    })
  } else if (currentMode.value === 'month') {
    const targetMonth = new Date(now.getFullYear(), now.getMonth() - dataStore.currentMonthOffset, 1)
    const startOfMonth = new Date(targetMonth.getFullYear(), targetMonth.getMonth(), 1)
    const endOfMonth = new Date(targetMonth.getFullYear(), targetMonth.getMonth() + 1, 0, 23, 59, 59, 999)
    
    filteredActivities = dataStore.activities.filter(a => {
      const activityDate = new Date(a.start_time)
      return activityDate >= startOfMonth && activityDate <= endOfMonth
    })
  } else if (currentMode.value === 'year') {
    const yearStart = new Date(dataStore.currentYear, 0, 1)
    const yearEnd = new Date(dataStore.currentYear, 11, 31)
    
    filteredActivities = dataStore.activities.filter(a => {
      const d = new Date(a.start_time)
      return d >= yearStart && d <= yearEnd
    })
  }
  
  // 计算总和
  const totalDistance = filteredActivities.reduce((sum, a) => sum + (a.distance || 0), 0) / 1000
  const totalDuration = filteredActivities.reduce((sum, a) => sum + (a.duration || 0), 0) / 60
  const totalCount = filteredActivities.length
  const totalCalories = filteredActivities.reduce((sum, a) => sum + (a.calories || 0), 0)
  
  // 计算平均速度
  const totalDistForSpeed = filteredActivities.reduce((sum, a) => sum + (a.distance || 0), 0)
  const totalDurForSpeed = filteredActivities.reduce((sum, a) => sum + (a.duration || 0), 0)
  const avgSpeed = totalDurForSpeed > 0 ? (totalDistForSpeed / totalDurForSpeed) * 3.6 : 0
  
  return [
    {
      label: '总距离',
      value: `${totalDistance.toFixed(2)} km`,
      gradient: 'linear-gradient(135deg, #3B82F6, #2563EB)',
      icon: '📍'
    },
    {
      label: '总时长',
      value: `${Math.round(totalDuration)} min`,
      gradient: 'linear-gradient(135deg, #F97316, #EA580C)',
      icon: '⏱️'
    },
    {
      label: '总次数',
      value: `${totalCount} 次`,
      gradient: 'linear-gradient(135deg, #8B5CF6, #7C3AED)',
      icon: '🎯'
    },
    {
      label: '总热量',
      value: `${Math.round(totalCalories)} kcal`,
      gradient: 'linear-gradient(135deg, #EF4444, #DC2626)',
      icon: '🔥'
    },
    {
      label: '平均速度',
      value: `${avgSpeed.toFixed(1)} km/h`,
      gradient: 'linear-gradient(135deg, #10B981, #059669)',
      icon: '⚡'
    }
  ]
})
function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
function updateChart() {
  if (!chartInstance) return

  const { data } = dataStore.processChartData(currentMode.value, currentMetric.value)
  const unit = getMetricUnit(currentMetric.value)

  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const dataPoint = params[0]
        const value = currentMetric.value === 'count' ? Math.round(dataPoint.value || 0) : (dataPoint.value?.toFixed(1) || 0)
        return `${dataPoint.name}<br/>${currentMetric.value === 'count' ? '次数' : '数值'}: ${value} ${unit}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.label),
      axisLabel: {
        color: '#6B7280',
        fontSize: 12,
        rotate: currentMode.value === 'all' ? 45 : 0
      },
      axisLine: {
        lineStyle: {
          color: '#E5E7EB'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: getAxisName(),
      nameTextStyle: {
        color: '#374151',
        fontSize: 13,
        fontWeight: 'bold'
      },
      axisLabel: {
        color: '#6B7280',
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: '#E5E7EB'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#E5E7EB',
          type: 'dashed'
        }
      }
    },
    series: [
      {
        data: data.map(d => d.value),
        type: 'bar',
        barWidth: '60%',
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#8B5CF6' },
              { offset: 1, color: '#6366F1' }
            ]
          },
          borderRadius: [4, 4, 0, 0]
        },
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(139, 92, 246, 0.1)',
          borderRadius: [4, 4, 0, 0]
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

function getAxisName(): string {
  switch (currentMetric.value) {
    case 'distance':
      return '距离 (km)'
    case 'duration':
      return '时长 (分钟)'
    case 'count':
      return '次数'
    case 'calories':
      return '热量 (kcal)'
    case 'avg_speed':
      return '速度 (km/h)'
    default:
      return ''
  }
}

function getMetricUnit(metric: ChartMetric): string {
  switch (metric) {
    case 'distance':
      return 'km'
    case 'duration':
      return '分钟'
    case 'count':
      return '次'
    case 'calories':
      return 'kcal'
    case 'avg_speed':
      return 'km/h'
    default:
      return ''
  }
}

function handleModeChange(mode: DisplayMode) {
  currentMode.value = mode
  // 切换模式时重置偏移量
  if (mode === 'week') {
    currentWeekOffset.value = 0
  } else if (mode === 'month') {
    currentMonthOffset.value = 0
  }
  dataStore.setDisplayMode(mode)
  updateChart()
}

function handleMetricChange(metric: ChartMetric) {
  currentMetric.value = metric
  dataStore.setChartMetric(metric)
  updateChart()
}

// 上一个周期
function previousPeriod() {
  if (currentMode.value === 'week') {
    currentWeekOffset.value++
    dataStore.setWeekOffset(currentWeekOffset.value)
  } else if (currentMode.value === 'month') {
    currentMonthOffset.value++
    dataStore.setMonthOffset(currentMonthOffset.value)
  } else if (currentMode.value === 'year') {
    const newYear = dataStore.currentYear - 1
    if (newYear >= minYear.value) {
      dataStore.setYear(newYear)
    }
  }
  updateChart()
}

// 下一个周期
function nextPeriod() {
  if (currentMode.value === 'week') {
    if (currentWeekOffset.value > 0) {
      currentWeekOffset.value--
      dataStore.setWeekOffset(currentWeekOffset.value)
    }
  } else if (currentMode.value === 'month') {
    if (currentMonthOffset.value > 0) {
      currentMonthOffset.value--
      dataStore.setMonthOffset(currentMonthOffset.value)
    }
  } else if (currentMode.value === 'year') {
    const newYear = dataStore.currentYear + 1
    if (newYear <= maxYear.value) {
      dataStore.setYear(newYear)
    }
  }
  updateChart()
}

watch(
  () => dataStore.activities,
  () => {
    updateChart()
  },
  { immediate: true }
)

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<style scoped>
.chart-view {
  padding: 0;
}

/* 卡片标题区域 */
.chart-header-section {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  background: #FFFFFF;
  border-radius: 16px 16px 0 0;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin: 0 0 16px 0;
}

.mode-selector-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.mode-selector {
  display: flex;
  gap: 4px;
}

.period-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.period-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  color: #6B7280;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background: #F9FAFB;
    border-color: #D1D5DB;
  }

  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}

.arrow {
  font-size: 18px;
  line-height: 1;
  font-weight: 300;
}

.period-input-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 12px;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  background: #FFFFFF;
  min-width: 120px;
  justify-content: center;

  &:focus-within {
    border-color: #8B5CF6;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  }
}

.period-input {
  width: 60px;
  border: none;
  outline: none;
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
  text-align: center;
  background: transparent;

  /* 移除数字输入框的上下箭头 */
  &::-webkit-inner-spin-button,
  &::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  -moz-appearance: textfield;
}

.period-label {
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
}

.mode-btn {
  padding: 6px 12px;
  font-size: 13px;
  border: none;
  background: transparent;
  color: #6B7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #F3F4F6;
  }

  &.active {
    background: #8B5CF6;
    color: #FFFFFF;
  }
}

/* 卡片内容区域 */
.chart-body {
  display: flex;
  gap: 16px;
  padding: 24px;
}

/* 左侧统计卡片列 */
.stats-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 240px;
  flex-shrink: 0;
}

/* 中间指标选择器 */
.metric-selector-vertical {
  padding: 0 8px;
  border-right: 1px solid #E5E7EB;
}

/* 右侧图表列 */
.chart-column {
  flex: 1;
  min-width: 0;
}

.chart-container {
  width: 100%;
  height: 400px;
}

@media (max-width: 1280px) {
  .stats-column {
    width: 240px;
  }
}

@media (max-width: 1024px) {
  .chart-body {
    flex-direction: column;
  }

  .stats-column {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .chart-header-section {
    padding: 16px 20px;
  }

  .chart-body {
    padding: 16px;
  }

  .chart-title {
    margin-bottom: 12px;
  }

  .chart-controls {
    flex-direction: column;
    width: 100%;
    align-items: stretch;
  }

  .mode-selector,
  .metric-selector {
    flex-wrap: wrap;
  }

  .stats-column {
    flex-direction: column;
  }

  .chart-container {
    height: 250px;
  }
}
</style>
