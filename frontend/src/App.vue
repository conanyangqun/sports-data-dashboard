<script setup lang="ts">
import { onMounted } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import AppHeader from '@/components/common/AppHeader.vue'
import Loading from '@/components/common/Loading.vue'

const dataStore = useDataStore()

onMounted(async () => {
  await dataStore.loadAllData()
})
</script>

<template>
  <div id="app">
    <AppHeader />
    <main class="main-content">
      <Loading v-if="dataStore.isLoading" message="加载中..." />
      <div v-else-if="dataStore.hasError" class="error-message">
        {{ dataStore.errorMessage }}
      </div>
      <router-view v-else />
    </main>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.main-content {
  min-height: calc(100vh - 80px);
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px);
  color: #EF4444;
  font-size: 16px;
}
</style>

