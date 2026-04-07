import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ActivityData, UserData } from '@/utils/json-reader'
import { loadData } from '@/utils/json-reader'

export type DisplayMode = 'week' | 'month' | 'year' | 'all'
export type ChartMetric = 'distance' | 'duration' | 'count' | 'calories' | 'avg_speed'
export type CalendarMetric = 'distance' | 'duration' | 'count' | 'calories' | 'avg_speed'

interface CalendarDayData {
  date: string
  value: number
  count: number
}

interface ChartDataPoint {
  label: string
  value: number
  count: number
}

interface WeekStats {
  totalDistance: number
  totalDuration: number
  totalCount: number
  totalCalories: number
  avgSpeed: number
}

export const useDataStore = defineStore('data', () => {
  // State
  const user = ref<UserData | null>(null)
  const activities = ref<ActivityData[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // 显示模式
  const currentMode = ref<DisplayMode>('week')
  const currentYear = ref<number>(new Date().getFullYear())
  const currentWeekOffset = ref<number>(0)
  const currentMonthOffset = ref<number>(0)
  
  // 指标选择
  const calendarMetric = ref<CalendarMetric>('distance')
  const chartMetric = ref<ChartMetric>('distance')

  // Getters
  const isLoading = computed(() => loading.value)
  const hasError = computed(() => error.value !== null)
  const errorMessage = computed(() => error.value)

  // Actions
  async function loadAllData() {
    loading.value = true
    error.value = null
    
    try {
      const data = await loadData()
      user.value = data.user
      activities.value = data.activities || []
      
      // 如果有数据，设置最新年份
      if (activities.value.length > 0) {
        const years = activities.value.map(a => new Date(a.start_time).getFullYear())
        currentYear.value = Math.max(...years)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载数据失败'
      console.error('Failed to load data:', err)
    } finally {
      loading.value = false
    }
  }

  // 计算最近 1 周统计数据
  function getWeekStats(): WeekStats {
    const now = new Date()
    const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    
    const recentActivities = activities.value.filter(a => {
      const activityDate = new Date(a.start_time)
      return activityDate >= oneWeekAgo
    })

    const totalDistance = recentActivities.reduce((sum, a) => sum + (a.distance || 0), 0)
    const totalDuration = recentActivities.reduce((sum, a) => sum + (a.duration || 0), 0)
    const totalCount = recentActivities.length
    const totalCalories = recentActivities.reduce((sum, a) => sum + (a.calories || 0), 0)
    
    // 计算平均速度（m/s 转换为 km/h）
    const avgSpeed = totalDuration > 0 
      ? (totalDistance / totalDuration) * 3.6 
      : 0

    return {
      totalDistance,
      totalDuration,
      totalCount,
      totalCalories,
      avgSpeed
    }
  }

  // 处理日历数据
  function processCalendarData(year: number, metric: CalendarMetric): CalendarDayData[] {
    const yearStart = new Date(year, 0, 1)
    const yearEnd = new Date(year, 11, 31)
    
    const filteredActivities = activities.value.filter(a => {
      const activityDate = new Date(a.start_time)
      return activityDate >= yearStart && activityDate <= yearEnd
    })

    // 按日期聚合数据
    const dateMap = new Map<string, CalendarDayData>()
    
    filteredActivities.forEach(activity => {
      const date = activity.start_time.split('T')[0]
      const existing = dateMap.get(date) || { date, value: 0, count: 0 }
      
      let value = 0
      switch (metric) {
        case 'distance':
          // 米转换为公里
          value = (activity.distance || 0) / 1000
          break
        case 'duration':
          // 秒转换为分钟
          value = (activity.duration || 0) / 60
          break
        case 'count':
          value = 1
          break
        case 'calories':
          // kcal，无需转换
          value = activity.calories || 0
          break
        case 'avg_speed':
          // m/s 转换为 km/h
          value = (activity.avg_speed || 0) * 3.6
          break
      }
      
      existing.value += value
      existing.count += 1
      dateMap.set(date, existing)
    })

    return Array.from(dateMap.values())
  }

  // 处理图表数据
  function processChartData(mode: DisplayMode, metric: ChartMetric): {
    stats: WeekStats
    data: ChartDataPoint[]
  } {
    let groupedActivities: Map<string, ActivityData[]> = new Map()
    
    // 根据模式分组
    const now = new Date()
    let filteredActivities = [...activities.value]
    
    if (mode === 'week') {
      // 根据周偏移计算目标周
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
      
      filteredActivities = activities.value.filter(a => {
        const activityDate = new Date(a.start_time)
        return activityDate >= startOfWeek && activityDate <= endOfWeek
      })
      
      // 初始化当周所有日期（确保即使没有数据也显示）
      for (let d = new Date(startOfWeek); d <= endOfWeek; d.setDate(d.getDate() + 1)) {
        const dateStr = `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`
        groupedActivities.set(dateStr, [])
      }
      
      // 按天分组
      filteredActivities.forEach(a => {
        const date = a.start_time.split('T')[0]
        const month = new Date(a.start_time).getMonth() + 1
        const day = new Date(a.start_time).getDate()
        const dateStr = `${String(month).padStart(2, '0')}/${String(day).padStart(2, '0')}`
        if (groupedActivities.has(dateStr)) {
          groupedActivities.get(dateStr)!.push(a)
        }
      })
    } else if (mode === 'month') {
      // 根据月偏移计算目标月
      const targetMonth = new Date(now.getFullYear(), now.getMonth() - currentMonthOffset.value, 1)
      const startOfMonth = new Date(targetMonth.getFullYear(), targetMonth.getMonth(), 1)
      const endOfMonth = new Date(targetMonth.getFullYear(), targetMonth.getMonth() + 1, 0, 23, 59, 59, 999)
      
      filteredActivities = activities.value.filter(a => {
        const activityDate = new Date(a.start_time)
        return activityDate >= startOfMonth && activityDate <= endOfMonth
      })
      
      // 初始化当月所有日期（确保即使没有数据也显示）
      const daysInMonth = endOfMonth.getDate()
      for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${String(targetMonth.getMonth() + 1).padStart(2, '0')}/${String(day).padStart(2, '0')}`
        groupedActivities.set(dateStr, [])
      }
      
      // 按天分组
      filteredActivities.forEach(a => {
        const date = a.start_time.split('T')[0]
        const month = new Date(a.start_time).getMonth() + 1
        const day = new Date(a.start_time).getDate()
        const dateStr = `${String(month).padStart(2, '0')}/${String(day).padStart(2, '0')}`
        if (groupedActivities.has(dateStr)) {
          groupedActivities.get(dateStr)!.push(a)
        }
      })
    } else if (mode === 'year') {
      const yearStart = new Date(currentYear.value, 0, 1)
      const yearEnd = new Date(currentYear.value, 11, 31)
      filteredActivities = activities.value.filter(a => {
        const d = new Date(a.start_time)
        return d >= yearStart && d <= yearEnd
      })
      
      // 初始化 12 个月（确保即使没有数据也显示）
      for (let month = 1; month <= 12; month++) {
        groupedActivities.set(`${month}月`, [])
      }
      
      // 按月分组
      filteredActivities.forEach(a => {
        const date = new Date(a.start_time)
        const month = date.getMonth() + 1
        const key = `${month}月`
        groupedActivities.get(key)!.push(a)
      })
    } else {
      // all - 按年分组
      filteredActivities.forEach(a => {
        const year = new Date(a.start_time).getFullYear().toString()
        if (!groupedActivities.has(year)) {
          groupedActivities.set(year, [])
        }
        groupedActivities.get(year)!.push(a)
      })
    }

    // 转换为图表数据
    const data: ChartDataPoint[] = Array.from(groupedActivities.entries())
      .sort(([a], [b]) => {
        // 年视图模式下按照月份数字排序（1-12 月）
        if (mode === 'year') {
          const monthA = parseInt(a.replace('月', ''))
          const monthB = parseInt(b.replace('月', ''))
          return monthA - monthB
        }
        return a.localeCompare(b)
      })
      .map(([label, acts]) => {
        let value = 0
        switch (metric) {
          case 'distance':
            // 米转换为公里
            value = acts.reduce((sum, a) => sum + (a.distance || 0), 0) / 1000
            break
          case 'duration':
            // 秒转换为分钟
            value = acts.reduce((sum, a) => sum + (a.duration || 0), 0) / 60
            break
          case 'count':
            value = acts.length
            break
          case 'calories':
            // kcal，无需转换
            value = acts.reduce((sum, a) => sum + (a.calories || 0), 0)
            break
          case 'avg_speed':
            // m/s 转换为 km/h
            const totalDist = acts.reduce((sum, a) => sum + (a.distance || 0), 0)
            const totalDur = acts.reduce((sum, a) => sum + (a.duration || 0), 0)
            value = totalDur > 0 ? (totalDist / totalDur) * 3.6 : 0
            break
        }
        return { label, value, count: acts.length }
      })

    // 计算统计数据
    const stats = getWeekStats()

    return { stats, data }
  }

  // 辅助函数：获取周数
  function getWeekNumber(date: Date): number {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
    const dayNum = d.getUTCDay() || 7
    d.setUTCDate(d.getUTCDate() + 4 - dayNum)
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
    return Math.ceil(((d.getTime() - yearStart.getTime()) / 86400000 + 1) / 7)
  }

  // 设置显示模式
  function setDisplayMode(mode: DisplayMode) {
    currentMode.value = mode
  }

  // 设置年份
  function setYear(year: number) {
    currentYear.value = year
  }

  // 设置日历指标
  function setCalendarMetric(metric: CalendarMetric) {
    calendarMetric.value = metric
  }

  // 设置图表指标
  function setChartMetric(metric: ChartMetric) {
    chartMetric.value = metric
  }

  // 设置周偏移量
  function setWeekOffset(offset: number) {
    currentWeekOffset.value = offset
  }

  // 设置月偏移量
  function setMonthOffset(offset: number) {
    currentMonthOffset.value = offset
  }

  return {
    // State
    user,
    activities,
    loading,
    error,
    currentMode,
    currentYear,
    currentWeekOffset,
    currentMonthOffset,
    calendarMetric,
    chartMetric,
    
    // Getters
    isLoading,
    hasError,
    errorMessage,
    
    // Actions
    loadAllData,
    getWeekStats,
    processCalendarData,
    processChartData,
    setDisplayMode,
    setYear,
    setCalendarMetric,
    setChartMetric,
    setWeekOffset,
    setMonthOffset
  }
})
