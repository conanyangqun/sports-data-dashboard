<template>
  <div class="app-card" :class="cardClass">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'default' | 'elevated' | 'outlined'
    padding?: 'none' | 'sm' | 'md' | 'lg'
  }>(),
  {
    variant: 'default',
    padding: 'md'
  }
)

const cardClass = computed(() => [
  `card-${props.variant}`,
  `p-${props.padding}`
])
</script>

<style scoped>
.app-card {
  background: #ffffff;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.card-default {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.card-elevated {
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);

  &:hover {
    box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
    transform: translateY(-4px);
  }
}

.card-outlined {
  border: 2px solid #e5e7eb;
  box-shadow: none;
}

.p-none {
  padding: 0;
}

.p-sm {
  padding: 12px;
}

.p-md {
  padding: 20px;
}

.p-lg {
  padding: 32px;
}
</style>
