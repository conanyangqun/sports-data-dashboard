<template>
  <div class="stat-card" :class="`stat-card-${variant}`">
    <div class="stat-icon" :style="{ background: gradient }">
      <span class="icon">{{ icon }}</span>
    </div>
    <div class="stat-content">
      <span class="stat-label">{{ label }}</span>
      <span class="stat-value">{{ value }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  icon: string
  gradient: string
  variant?: 'default' | 'mini'
}>()
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #FFFFFF;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-card-mini {
  padding: 12px;
  gap: 10px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.stat-card-mini .stat-icon {
  width: 36px;
  height: 36px;
  font-size: 18px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stat-label {
  font-size: 13px;
  color: #6B7280;
  font-weight: 500;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1F2937;
  white-space: nowrap;
}

.stat-card-mini .stat-value {
  font-size: 16px;
}
</style>
