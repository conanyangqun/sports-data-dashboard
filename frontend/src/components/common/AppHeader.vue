<template>
  <header class="app-header">
    <div class="user-info">
      <img v-if="user?.avatar_url" :src="user.avatar_url" :alt="user.display_name || user.username" class="avatar" />
      <div v-else class="avatar-placeholder">
        <span>{{ (user?.display_name || user?.username)?.charAt(0)?.toUpperCase() || 'U' }}</span>
      </div>
      <div class="user-details">
        <h2 class="username">{{ user?.display_name || user?.username || '用户' }}</h2>
        <p class="bio">{{ user?.bio || '运动爱好者' }}</p>
      </div>
    </div>
    <nav class="nav-menu">
      <router-link to="/" class="nav-item" active-class="active">
        仪表盘
      </router-link>
      <router-link to="/activities" class="nav-item" active-class="active">
        运动记录
      </router-link>
      <a href="#" class="nav-item" @click.prevent="showMapWarning">
        地图
      </a>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDataStore } from '@/stores/dataStore'

const dataStore = useDataStore()
const user = computed(() => dataStore.user)

function showMapWarning() {
  alert('地图页面正在开发中，敬请期待！')
}
</script>

<style scoped>
.app-header {
  height: 80px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 600;
  font-size: 20px;
}

.user-details {
  color: #ffffff;
}

.username {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.bio {
  font-size: 14px;
  font-weight: 400;
  margin: 0;
  opacity: 0.8;
}

.nav-menu {
  display: flex;
  gap: 32px;
}

.nav-item {
  font-size: 15px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 8px 0;
  transition: all 0.2s ease;
  border-bottom: 2px solid transparent;

  &:hover {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.1);
  }

  &.active {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.2);
    border-bottom-color: #ffffff;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
  }

  .bio {
    display: none;
  }

  .nav-menu {
    gap: 16px;
  }
}
</style>
