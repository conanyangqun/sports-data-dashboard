<template>
  <div class="dashboard">
    <!-- 上半部分 -->
    <div class="dashboard-top">
      <!-- 左侧：周统计 -->
      <div class="weekly-stats-section">
        <AppCard class="weekly-stats-card" padding="none">
          <div class="stats-header">
            <h3 class="stats-title">最近 1 周 <span class="week-range">{{ weekRangeLabel }}</span></h3>
          </div>
          <div class="stats-body">
            <StatsPanel
              :stats="weekStats"
              variant="mini"
            />
          </div>
        </AppCard>
      </div>
      
      <!-- 右侧：日历图 -->
      <div class="calendar-section">
        <CalendarView />
      </div>
    </div>
    
    <!-- 下半部分：柱形图 -->
    <div class="dashboard-bottom">
      <ChartView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import CalendarView from '@/components/dashboard/CalendarView.vue'
import ChartView from '@/components/dashboard/ChartView.vue'
import AppCard from '@/components/common/AppCard.vue'
import StatCard from '@/components/common/StatCard.vue'
import StatsPanel from '@/components/common/StatsPanel.vue'

const dataStore = useDataStore()

// 计算本周日期范围
const weekRangeLabel = computed(() => {
  const now = new Date()
  const startOfWeek = new Date(now)
  // 周一作为一周的开始：getDay() 返回 0(周日) 时，需要减去 6 天；返回 1(周一) 时，减去 0 天
  const day = now.getDay()
  const diff = day === 0 ? 6 : day - 1
  startOfWeek.setDate(now.getDate() - diff)
  const endOfWeek = new Date(startOfWeek)
  endOfWeek.setDate(startOfWeek.getDate() + 6)
  
  const format = (date: Date) => {
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${month}/${day}`
  }
  
  return `(${format(startOfWeek)} - ${format(endOfWeek)})`
})

const weekStats = computed(() => {
  const stats = dataStore.getWeekStats()
  return [
    {
      label: '总距离',
      value: `${(stats.totalDistance / 1000).toFixed(2)} km`,
      gradient: 'linear-gradient(135deg, #3B82F6, #2563EB)',
      icon: '📍'
    },
    {
      label: '总时长',
      value: `${Math.round(stats.totalDuration / 60)} min`,
      gradient: 'linear-gradient(135deg, #F97316, #EA580C)',
      icon: '⏱️'
    },
    {
      label: '总次数',
      value: `${stats.totalCount} 次`,
      gradient: 'linear-gradient(135deg, #8B5CF6, #7C3AED)',
      icon: '🎯'
    },
    {
      label: '总热量',
      value: `${Math.round(stats.totalCalories)} kcal`,
      gradient: 'linear-gradient(135deg, #EF4444, #DC2626)',
      icon: '🔥'
    },
    {
      label: '平均速度',
      value: `${stats.avgSpeed.toFixed(1)} km/h`,
      gradient: 'linear-gradient(135deg, #10B981, #059669)',
      icon: '⚡'
    }
  ]
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px;
  background: #F9FAFB;
  min-height: calc(100vh - 80px);
}

.dashboard-top {
  display: flex;
  gap: 24px;
  align-items: stretch;
}

.weekly-stats-section {
  flex: 1;
  max-width: 25%;
}

.weekly-stats-card {
  height: 100%;
}

.calendar-section {
  flex: 1;
  max-width: 75%;
  min-height: 0;
}

.stats-header {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E7EB;
  background: #FFFFFF;
  border-radius: 16px 16px 0 0;
}

.stats-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.week-range {
  font-size: 14px;
  font-weight: 400;
  color: #6B7280;
}

.stats-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}



.dashboard-bottom {
  width: 100%;
}

@media (max-width: 1024px) {
  .dashboard-top {
    flex-direction: column;
  }

  .weekly-stats-section {
    max-width: 100%;
  }

  .calendar-section {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .stats-body {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
