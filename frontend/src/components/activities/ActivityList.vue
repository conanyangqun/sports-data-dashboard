<template>
  <AppCard class="activity-list">
    <div class="activity-header">
      <h3 class="activity-title">运动记录</h3>
      <div class="activity-filters">
        <select v-model="filterType" class="filter-select">
          <option value="">全部类型</option>
          <option value="riding">骑行</option>
          <option value="running">跑步</option>
          <option value="swimming">游泳</option>
          <option value="walking">健走</option>
          <option value="hiking">徒步</option>
          <option value="other">其他</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="activity-table">
        <thead>
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="{ sortable: column.sortable, 'sorted-asc': sortKey === column.key && sortOrder === 'asc', 'sorted-desc': sortKey === column.key && sortOrder === 'desc' }"
              @click="column.sortable && handleSort(column.key)"
            >
              {{ column.label }}
              <span v-if="column.sortable" class="sort-icon">
                {{ sortKey === column.key ? (sortOrder === 'asc' ? '↑' : '↓') : '↕' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="activity in paginatedData" :key="activity.id">
            <td>{{ formatDate(activity.start_time) }}</td>
            <td>{{ getActivityType(activity.activity_type) }}</td>
            <td>{{ formatDistance(activity.distance) }}</td>
            <td>{{ formatDuration(activity.duration) }}</td>
            <td>{{ formatValue(activity.calories) }}</td>
            <td>{{ formatSpeed(activity.avg_speed) }}</td>
            <td>{{ formatSpeed(activity.max_speed) }}</td>
            <td>{{ formatValue(activity.avg_heart_rate) }}</td>
            <td>{{ formatValue(activity.max_heart_rate) }}</td>
            <td>{{ formatValue(activity.avg_cadence) }}</td>
            <td>{{ formatValue(activity.max_cadence) }}</td>
          </tr>
          <tr v-if="filteredData.length === 0">
            <td :colspan="columns.length" class="empty-message">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <div class="pagination-info">
        显示 {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, filteredData.length) }} 条，共 {{ filteredData.length }} 条
      </div>
      <div class="pagination-controls">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          上一页
        </button>
        <button
          v-for="page in visiblePages"
          :key="page"
          :class="['page-number', { active: page === currentPage }]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
        <button 
          class="page-btn" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          下一页
        </button>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import AppCard from '@/components/common/AppCard.vue'
import { useDataStore } from '@/stores/dataStore'
import type { ActivityData } from '@/utils/json-reader'

const dataStore = useDataStore()

interface Column {
  key: keyof ActivityData | string
  label: string
  sortable: boolean
}

const columns: Column[] = [
  { key: 'start_time', label: '运动日期', sortable: true },
  { key: 'activity_type', label: '运动类型', sortable: true },
  { key: 'distance', label: '距离 (km)', sortable: true },
  { key: 'duration', label: '时长', sortable: true },
  { key: 'calories', label: '热量 (kcal)', sortable: true },
  { key: 'avg_speed', label: '平均速度 (km/h)', sortable: true },
  { key: 'max_speed', label: '最大速度 (km/h)', sortable: true },
  { key: 'avg_heart_rate', label: '平均心率', sortable: true },
  { key: 'max_heart_rate', label: '最大心率', sortable: true },
  { key: 'avg_cadence', label: '平均踏频', sortable: true },
  { key: 'max_cadence', label: '最大踏频', sortable: true }
]

const filterType = ref('')
const sortKey = ref<keyof ActivityData | string>('start_time')
const sortOrder = ref<'asc' | 'desc'>('desc')
const currentPage = ref(1)
const pageSize = ref(20)

// 过滤数据
const filteredData = computed(() => {
  let data = [...dataStore.activities]
  
  if (filterType.value) {
    data = data.filter(a => a.activity_type === filterType.value)
  }
  
  // 排序
  data.sort((a, b) => {
    const aVal = a[sortKey.value as keyof ActivityData]
    const bVal = b[sortKey.value as keyof ActivityData]
    
    if (aVal === null || aVal === undefined) return 1
    if (bVal === null || bVal === undefined) return -1
    
    const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0
    return sortOrder.value === 'asc' ? comparison : -comparison
  })
  
  return data
})

// 分页数据
const totalPages = computed(() => Math.ceil(filteredData.value.length / pageSize.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})

// 可见页码
const visiblePages = computed(() => {
  const pages: number[] = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// 格式化函数
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getActivityType(type: string): string {
  const typeMap: Record<string, string> = {
    cycling: '骑行',
    riding: '骑行',
    running: '跑步',
    swimming: '游泳',
    walking: '健走',
    hiking: '徒步',
    other: '其他'
  }
  return typeMap[type] || type
}

function formatDistance(meters: number | null): string {
  if (meters === null || meters === undefined) return '-'
  return `${(meters / 1000).toFixed(2)} km`
}

function formatDuration(seconds: number | null): string {
  if (seconds === null || seconds === undefined) return '-'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  }
  return `${minutes}m`
}

function formatValue(value: number | null): string {
  if (value === null || value === undefined) return '-'
  return value.toFixed(0)
}

function formatSpeed(speed: number | null): string {
  if (speed === null || speed === undefined) return '-'
  // 假设速度单位是 m/s，转换为 km/h
  return (speed * 3.6).toFixed(1)
}

// 排序处理
function handleSort(key: keyof ActivityData | string) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'desc'
  }
}

// 监听过滤变化，重置页码
watch(filterType, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.activity-list {
  padding: 24px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
}

.activity-filters {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  color: #1F2937;
  cursor: pointer;
}

.table-container {
  overflow-x: auto;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
}

.activity-table th,
.activity-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #F3F4F6;
  font-size: 14px;
  white-space: nowrap;
}

.activity-table th {
  background: #F9FAFB;
  font-weight: 600;
  color: #6B7280;
  cursor: default;
  
  &.sortable {
    cursor: pointer;
    user-select: none;
    
    &:hover {
      background: #F3F4F6;
    }
  }
  
  &.sorted-asc,
  &.sorted-desc {
    background: #EFF6FF;
    color: #8B5CF6;
  }
}

.sort-icon {
  margin-left: 4px;
  font-size: 12px;
  opacity: 0.6;
}

.activity-table tbody tr {
  transition: background-color 0.2s ease;
  
  &:hover {
    background: #F9FAFB;
  }
}

.empty-message {
  text-align: center;
  color: #9CA3AF;
  padding: 40px !important;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #E5E7EB;
}

.pagination-info {
  font-size: 14px;
  color: #6B7280;
}

.pagination-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.page-btn,
.page-number {
  padding: 8px 16px;
  font-size: 14px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  color: #6B7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover:not(:disabled) {
    background: #F3F4F6;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  &.active {
    background: #8B5CF6;
    color: #FFFFFF;
    border-color: #8B5CF6;
  }
}

@media (max-width: 1024px) {
  .activity-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
