<template>
  <div class="metric-selector-vertical">
    <button
      v-for="item in items"
      :key="item.value"
      :class="['metric-btn-vertical', { active: modelValue === item.value }]"
      @click="$emit('update:modelValue', item.value)"
      :title="item.label"
    >
      <span class="metric-icon">{{ item.icon }}</span>
      <span class="metric-label">{{ item.label }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
interface MetricItem {
  label: string
  value: string
  icon?: string
}

defineProps<{
  items: MetricItem[]
  modelValue: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped>
.metric-selector-vertical {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-btn-vertical {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  color: #6B7280;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;

  &:hover {
    background: #F9FAFB;
    border-color: #D1D5DB;
  }

  &.active {
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
    color: #FFFFFF;
    border-color: #8B5CF6;
    box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3);
  }
}

.metric-icon {
  font-size: 20px;
  line-height: 1;
}

.metric-label {
  font-size: 12px;
  font-weight: 500;
}
</style>
