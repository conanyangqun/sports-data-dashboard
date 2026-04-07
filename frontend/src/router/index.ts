import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Activities from '../views/Activities.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/activities',
    name: 'Activities',
    component: Activities
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
