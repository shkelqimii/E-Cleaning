import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Index from '../views/Index.vue'
import Navbar from '../views/Navbar.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/index',
    name: 'Index',
    component: Index
  },
  {
    path: '/navbar',
    name: 'Navbar',
    component: Navbar
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
    const publicPages = ['/', '/register'];  // List of routes that are public
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('authToken');

    if (authRequired && !loggedIn) {
        return next('/');
    }
    next();
});

export default router;
