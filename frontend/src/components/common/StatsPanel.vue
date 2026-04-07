<template>
  <div class="stats-panel">
    <div v-show="title" class="stats-panel-title">
      {{ title }}
    </div>
    <div class="stats-panel-body">
      <StatCard
        v-for="stat in stats"
        :key="stat.label"
        :label="stat.label"
        :value="stat.value"
        :icon="stat.icon"
        :gradient="stat.gradient"
        :variant="variant"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import StatCard from './StatCard.vue'

interface StatItem {
  label: string
  value: string
  icon: string
  gradient: string
}

defineProps<{
  title?: string
  stats: StatItem[]
  variant?: 'default' | 'mini'
}>()
</script>

<style scoped>
.stats-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stats-panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
  padding: 0 4px;
}

.stats-panel-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
