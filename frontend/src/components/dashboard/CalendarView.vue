<template>
  <AppCard class="calendar-view" padding="none">
    <!-- 卡片标题区域 -->
    <div class="calendar-header-section">
      <h3 class="calendar-main-title">运动日历</h3>
    </div>
    
    <!-- 卡片内容区域 -->
    <div class="calendar-body">
      <!-- 左侧指标选择 -->
      <MetricSelector
        v-model="currentMetric"
        :items="metricItems"
        @update:modelValue="handleMetricChange"
      />
      
      <!-- 右侧日历区域 -->
      <div class="calendar-content">
        <div class="calendar-controls">
          <div class="year-controls">
            <button class="year-btn" @click="previousYear" :disabled="!canPreviousYear">
              <span class="arrow">‹</span>
            </button>
            <div class="year-picker-wrapper" ref="yearPickerRef" @click="togglePicker">
              <input 
                type="text" 
                :value="inputYear"
                class="year-picker-input"
                readonly
              />
              <span class="year-label">年</span>
              <span class="picker-icon">📅</span>
            </div>
            <button class="year-btn" @click="nextYear" :disabled="!canNextYear">
              <span class="arrow">›</span>
            </button>
          </div>
        </div>
        
        <!-- 年份选择器弹窗 -->
        <Teleport to="body">
          <div v-if="showPicker" class="year-picker-dropdown" :style="pickerStyle" @click.stop>
            <div class="picker-header">
              <button class="picker-nav-btn" @click="currentPickerPage--" :disabled="currentPickerPage <= 0">
                <span class="arrow">‹</span>
              </button>
              <span class="picker-range-label">{{ pickerStartYear }} - {{ pickerEndYear }}</span>
              <button class="picker-nav-btn" @click="currentPickerPage++" :disabled="currentPickerPage >= totalPickerPages - 1">
                <span class="arrow">›</span>
              </button>
            </div>
            <div class="picker-body">
              <div class="year-grid">
                <div 
                  v-for="year in displayedYears" 
                  :key="year"
                  :class="['year-cell', { current: year === inputYear }]"
                  @click="selectYear(year)"
                >
                  {{ year }}
                </div>
              </div>
            </div>
          </div>
        </Teleport>
        
        <div ref="chartRef" class="calendar-chart"></div>
        
        <div class="calendar-legend">
          <div class="legend-item">
            <span class="legend-color" style="background-color: #F3F4F6;"></span>
            <span class="legend-label">无数据</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: #DBEAFE;"></span>
            <span class="legend-label">低</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: #93C5FD;"></span>
            <span class="legend-label">中</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: #3B82F6;"></span>
            <span class="legend-label">高</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: #2563EB;"></span>
            <span class="legend-label">极高</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: rgba(239, 68, 68, 0.3); border: 2px solid #EF4444; border-radius: 2px;"></span>
            <span class="legend-label">今天</span>
          </div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import AppCard from '@/components/common/AppCard.vue'
import MetricSelector from '@/components/common/MetricSelector.vue'
import { useDataStore } from '@/stores/dataStore'
import type { CalendarMetric } from '@/stores/dataStore'

const dataStore = useDataStore()
const chartRef = ref<HTMLElement | null>(null)
const yearPickerRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const selectedYear = ref<number>(new Date().getFullYear())
const inputYear = ref<number>(new Date().getFullYear())
const currentMetric = ref<CalendarMetric>('distance')

// 年份选择器状态
const showPicker = ref<boolean>(false)
const currentPickerPage = ref<number>(0)
const pickerStyle = ref<{ top: string; left: string }>({ top: '0px', left: '0px' })
const yearsPerPage = 12

const metrics = [
  { label: '距离', value: 'distance' as CalendarMetric, icon: '📍' },
  { label: '时长', value: 'duration' as CalendarMetric, icon: '⏱️' },
  { label: '次数', value: 'count' as CalendarMetric, icon: '🎯' },
  { label: '热量', value: 'calories' as CalendarMetric, icon: '🔥' },
  { label: '均速', value: 'avg_speed' as CalendarMetric, icon: '⚡' }
]

// 指标选项
const metricItems = computed(() => metrics)

// 年仹范围
const minYear = computed(() => {
  const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
  return years.length > 0 ? Math.min(...years) : new Date().getFullYear() - 1
})

const maxYear = computed(() => {
  const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
  return years.length > 0 ? Math.max(...years) : new Date().getFullYear()
})

// 是否可以翻页
const canPreviousYear = computed(() => selectedYear.value > minYear.value)
const canNextYear = computed(() => selectedYear.value < maxYear.value)

// 年份选择器相关计算属性
const pickerStartYear = computed(() => {
  return minYear.value + currentPickerPage.value * yearsPerPage
})

const pickerEndYear = computed(() => {
  const end = pickerStartYear.value + yearsPerPage - 1
  return Math.min(end, maxYear.value)
})

const totalPickerPages = computed(() => {
  const totalYears = maxYear.value - minYear.value + 1
  return Math.ceil(totalYears / yearsPerPage)
})

const displayedYears = computed(() => {
  const years: number[] = []
  const start = pickerStartYear.value
  const end = pickerEndYear.value
  for (let year = start; year <= end; year++) {
    years.push(year)
  }
  return years
})

// 初始化图表
function initChart() {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
function updateChart() {
  if (!chartInstance) return
  
  const calendarData = dataStore.processCalendarData(selectedYear.value, currentMetric.value)
  
  // 获取今天的日期
  const today = new Date()
  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
  
  // 检查今天是否已经在数据中
  const hasToday = calendarData.some(item => item.date === todayStr)
  
  // 如果今天不在数据中且今天是当前年份，添加今天的空数据
  if (!hasToday && today.getFullYear() === selectedYear.value) {
    calendarData.push({
      date: todayStr,
      value: 0,
      count: 0
    })
  }
  
  // 格式化数据为 ECharts 日历格式，并为今天设置特殊颜色
  const formattedData = calendarData.map(item => {
    const isToday = item.date === todayStr
    return {
      value: [item.date, item.value],
      itemStyle: isToday ? {
        color: 'rgba(239, 68, 68, 0.3)', // 红色背景突出显示今天
        borderColor: '#EF4444',
        borderWidth: 2
      } : undefined
    }
  })
  
  // 获取度量单位
  const unit = getMetricUnit(currentMetric.value)
  
  const option: EChartsOption = {
    tooltip: {
      formatter: (params: any) => {
        const date = params.data.value ? params.data.value[0] : params.data[0]
        const value = params.data.value ? params.data.value[1] : params.data[1]
        const isToday = date === todayStr ? ' (今天)' : ''
        const displayValue = currentMetric.value === 'count' ? Math.round(value || 0) : (value?.toFixed(1) || 0)
        return `${date}${isToday}<br/>${currentMetric.value === 'count' ? '次数' : '数值'}: ${displayValue} ${unit}`
      }
    },
    visualMap: {
      min: 0,
      max: getMaxValue(calendarData),
      calculable: true,
      inRange: {
        color: ['#DBEAFE', '#93C5FD', '#3B82F6', '#2563EB', '#1E40AF']
      },
      show: false
    },
    calendar: {
      top: 30,
      left: 30,
      right: 30,
      bottom: 30,
      cellSize: ['auto', 14],
      yearLabel: { show: false },
      dayLabel: {
        nameMap: 'cn',
        color: '#6B7280',
        fontSize: 11
      },
      monthLabel: {
        nameMap: 'cn',
        color: '#6B7280',
        fontSize: 12
      },
      splitLine: {
        show: false
      },
      itemStyle: {
        borderRadius: 3,
        borderWidth: 1,
        borderColor: '#E5E7EB'
      },
      range: selectedYear.value.toString()
    },
    series: {
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: formattedData,
      itemStyle: {
        borderRadius: 3
      }
    }
  }
  
  chartInstance.setOption(option)
}

// 获取最大值用于颜色映射
function getMaxValue(data: any[]): number {
  if (data.length === 0) return 100
  const max = Math.max(...data.map(d => d.value))
  return max > 0 ? max : 100
}

// 获取度量单位
function getMetricUnit(metric: CalendarMetric): string {
  switch (metric) {
    case 'distance':
      return '公里'
    case 'duration':
      return '分钟'
    case 'count':
      return '次'
    case 'calories':
      return '千卡'
    case 'avg_speed':
      return 'km/h'
    default:
      return ''
  }
}

// 上一年
function previousYear() {
  if (canPreviousYear.value) {
    selectedYear.value--
    inputYear.value = selectedYear.value
    dataStore.setYear(selectedYear.value)
    updateChart()
  }
}

// 下一年
function nextYear() {
  if (canNextYear.value) {
    selectedYear.value++
    inputYear.value = selectedYear.value
    dataStore.setYear(selectedYear.value)
    updateChart()
  }
}

// 切换选择器显示
function togglePicker() {
  showPicker.value = !showPicker.value
  if (showPicker.value) {
    nextTick(() => {
      updatePickerPosition()
    })
  }
}

// 更新选择器位置
function updatePickerPosition() {
  if (!yearPickerRef.value) return
  
  const rect = yearPickerRef.value.getBoundingClientRect()
  pickerStyle.value = {
    top: `${rect.bottom + window.scrollY + 8}px`,
    left: `${rect.left + window.scrollX}px`
  }
}

// 选择年份
function selectYear(year: number) {
  selectedYear.value = year
  inputYear.value = year
  dataStore.setYear(year)
  showPicker.value = false
  updateChart()
}

// 处理年份输入
function handleYearInput() {
  const year = inputYear.value
  if (year >= minYear.value && year <= maxYear.value) {
    selectedYear.value = year
    dataStore.setYear(year)
    updateChart()
  } else {
    // 如果输入超出范围，恢复到当前年份
    inputYear.value = selectedYear.value
  }
}

// 处理指标切换
function handleMetricChange(metric: string) {
  currentMetric.value = metric as CalendarMetric
  dataStore.setCalendarMetric(metric as CalendarMetric)
  updateChart()
}

// 监听数据变化
watch(
  () => dataStore.activities,
  () => {
    if (dataStore.activities.length > 0) {
      const years = dataStore.activities.map(a => new Date(a.start_time).getFullYear())
      const maxYear = Math.max(...years)
      selectedYear.value = maxYear
      inputYear.value = maxYear
      updateChart()
    }
  },
  { immediate: true }
)

// 初始化
onMounted(() => {
  initChart()
  
  // 窗口大小变化时重新渲染
  window.addEventListener('resize', handleResize)
  
  // 点击外部关闭选择器
  document.addEventListener('click', handleOutsideClick)
})

// 清理函数
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('click', handleOutsideClick)
  chartInstance?.dispose()
  chartInstance = null
})

// 窗口大小变化处理函数
function handleResize() {
  chartInstance?.resize()
}

// 点击外部关闭选择器处理函数
function handleOutsideClick(e: Event) {
  if (showPicker.value && yearPickerRef.value && !yearPickerRef.value.contains(e.target as Node)) {
    showPicker.value = false
  }
}
</script>

<style scoped>
.calendar-view {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 卡片标题区域 */
.calendar-header-section {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  background: #FFFFFF;
  border-radius: 16px 16px 0 0;
}

.calendar-main-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
}

/* 卡片内容区域 */
.calendar-body {
  display: flex;
  gap: 16px;
  padding: 24px;
  flex: 1;
  min-height: 0;
}

/* 右侧日历内容 */
.calendar-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 0;
}

.calendar-controls {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.year-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.year-btn {
  width: 32px;
  height: 32px;
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
  font-size: 20px;
  line-height: 1;
  font-weight: 300;
}

.year-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 12px;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;

  &:hover {
    border-color: #D1D5DB;
    background: #F9FAFB;
  }
}

.year-picker-input {
  width: 60px;
  border: none;
  outline: none;
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
  text-align: center;
  background: transparent;
  cursor: pointer;
}

.year-label {
  font-size: 14px;
  color: #6B7280;
}

.picker-icon {
  font-size: 14px;
  margin-left: 2px;
}

/* 年份选择器弹窗样式 */
.year-picker-dropdown {
  position: absolute;
  z-index: 2000;
  background: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #E5E7EB;
  padding: 12px;
  min-width: 220px;
  animation: fade-in 0.2s ease;
}

.picker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #E5E7EB;
}

.picker-range-label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.picker-nav-btn {
  width: 24px;
  height: 24px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  color: #6B7280;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background: #F3F4F6;
    border-color: #D1D5DB;
  }

  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}

.year-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
}

.year-cell {
  padding: 8px 12px;
  border-radius: 6px;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #F3F4F6;
  }

  &.current {
    background: #3B82F6;
    color: #FFFFFF;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.calendar-chart {
  width: 100%;
  flex: 1;
  min-height: 0;
}

.calendar-legend {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-label {
  font-size: 12px;
  color: #6B7280;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .calendar-body {
    flex-direction: column;
  }

  .metric-selector-vertical {
    flex-direction: row;
    padding-right: 0;
    border-right: none;
    border-bottom: 1px solid #E5E7EB;
    padding-bottom: 16px;
    overflow-x: auto;
  }

  .metric-btn-vertical {
    flex-direction: row;
    gap: 8px;
    min-width: auto;
    padding: 8px 16px;
  }

  .metric-label {
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .calendar-header-section {
    padding: 16px 20px;
  }

  .calendar-body {
    padding: 16px;
  }

  .calendar-controls {
    width: 100%;
  }

  .year-controls {
    width: 100%;
    justify-content: center;
  }

  .calendar-chart {
    flex: 1;
    min-height: 200px;
  }

  .calendar-legend {
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>
