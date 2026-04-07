<template>
  <div class="activities-page">
    <ActivityList />
  </div>
</template>

<script setup lang="ts">
import ActivityList from '@/components/activities/ActivityList.vue'
</script>

<style scoped>
.activities-page {
  padding: 32px;
  background: #F9FAFB;
  min-height: calc(100vh - 80px);
}
</style>
