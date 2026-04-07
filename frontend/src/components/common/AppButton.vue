<template>
  <button class="app-button" :class="buttonClass" :disabled="disabled" @click="$emit('click', $event)">
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'danger'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
  }>(),
  {
    variant: 'primary',
    size: 'md',
    disabled: false
  }
)

defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClass = computed(() => [
  `btn-${props.variant}`,
  `btn-${props.size}`
])
</script>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.btn-primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #f97316 100%);
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);

  &:hover:not(:disabled) {
    box-shadow: 0 4px 8px rgba(139, 92, 246, 0.4);
    transform: translateY(-2px);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
  }
}

.btn-secondary {
  background: #ffffff;
  color: #6b7280;
  border: 1px solid #e5e7eb;

  &:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #d1d5db;
  }
}

.btn-danger {
  background: #ef4444;
  color: #ffffff;

  &:hover:not(:disabled) {
    background: #dc2626;
  }
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}

.btn-md {
  padding: 10px 20px;
  font-size: 14px;
}

.btn-lg {
  padding: 12px 24px;
  font-size: 16px;
}
</style>
