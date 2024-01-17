import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Index from '../views/Index.vue'
import Navbar from '../views/Navbar.vue'
import Profile from '../views/Profile.vue'
import Workers from '../views/Workers.vue'
import Clients from '../views/Clients.vue'
import ProductForm from '../views/ProductForm.vue';  // Import this
import ProductsList from '../views/ProductsList.vue';  // Import this
import ProductDetail from '../views/ProductDetail.vue';  // Import this
import EditProduct from '../views/EditProduct.vue';  // Import the component
import Cart from '../views/Cart.vue';
import PaymentSuccess from '@/views/PaymentSuccess.vue';
import PaymentCancelled from '@/views/PaymentCancelled.vue';
import Notifications from '@/views/Notifications.vue';
import WashproductsForm from '@/views/WashproductsForm.vue';
import WashproductDetail from '../views/WashproductDetail.vue'; // Adjust the path as per your project structure
import WashproductEdit from '@/views/WashproductEdit.vue';
import SuccessPage from '@/views/SuccessPage.vue'; 
import QRCodes from '@/views/QRCodes.vue';



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
  },
  {
    path: '/workers',
    name: 'Workers',
    component: Workers
  },
  {
    path: '/clients',
    name: 'Clients',
    component: Clients
  },
  {
    path: '/add-product',
    name: 'AddProduct',
    component: ProductForm
  },
  {
    path: '/products',
    name: 'ProductsList',
    component: ProductsList
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: ProductDetail
  },
  {
    path: '/productForm',
    name: 'ProductForm',
    component: ProductForm
  },
  {
    path: '/edit-product/:id',
    name: 'EditProduct',
    component: EditProduct
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/success',
    name: 'PaymentSuccess',
    component: PaymentSuccess,
  },
  {
    path: '/cancelled',
    name: 'PaymentCancelled',
    component: PaymentCancelled,
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications
  },
  {
    path: '/add-washproduct',
    name: 'AddWashproduct',
    component: WashproductsForm
  },
  {
    path: '/washproducts/:id',
    name: 'WashproductDetail',
    component: WashproductDetail
  },
  {
    path: '/washproducts/edit/:id', // Use a dynamic segment for the wash product ID
    name: 'WashproductEdit',
    component: WashproductEdit,
    props: true // This allows the id to be passed as a prop to the component
  },

  {
    path: '/success-page',
    name: 'SuccessPage',
    component: SuccessPage
  },
  {
    path: '/qrcodes',
    name: 'QRCodes',
    component: QRCodes
  },


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
