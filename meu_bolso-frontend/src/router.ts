import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Home from './views/Home.vue'
import Analytics from './views/Analytics.vue'
import NewExpense from './views/NewExpense.vue'
import { useAuthStore } from './stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login },
    { 
      path: '/', 
      component: Home,
      meta: { requiresAuth: true }
    },
    { 
      path: '/analytics', 
      component: Analytics,
      meta: { requiresAuth: true }
    },
    { 
      path: '/new-expense', 
      component: NewExpense,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router