<template>
  <nav :class="isDarkMode ? 'bg-gradient-to-r from-violet-900 to-blue-900' : 'bg-gradient-to-r from-violet-300 to-blue-300'" class="shadow-lg transition-all duration-500 fixed bottom-0 w-full flex justify-center items-center p-1 mx-auto nav-z-index">


    <!-- Left: User Profile Button (positioned absolutely) -->

    <router-link to="/cart" class=" flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full absolute left-4 bottom-2">
        <font-awesome-icon icon="cart-shopping" class="text-xl text-white" />
        <span v-if="totalCartItems > 0" class="absolute bottom-8 left-7 bg-red-500 text-white text-xm rounded-full w-7 h-7 flex items-center justify-center">{{ totalCartItems }}</span>
    </router-link>


    <router-link to="/products" class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500  hover:shadow-lg rounded-full absolute left-20 bottom-2">
        <font-awesome-icon icon="shop" class="text-xl text-white" />
    </router-link>


    <!-- Center: Home Link -->
    <router-link 
        to="/index" 
        :class="isDarkMode ? 'text-gray-700' : 'text-white'"
        class="w-20 h-16 flex items-center justify-center bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full"
    >
        <font-awesome-icon icon="house" class="text-xl" />
    </router-link>

    <router-link to="/notifications/" class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full absolute right-20 bottom-2">
      <font-awesome-icon icon="newspaper" class="text-xl text-white" />
    </router-link>
    



    <!-- Right: Options Button (positioned absolutely) -->
    <button ref="optionsButton" @click.stop="toggleOptions" class="w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full absolute right-4 bottom-2">
        <font-awesome-icon icon="gear" class="text-xl text-white" />
    </button>
    

    <!-- Dropdown with Logout and Dark Mode Toggle -->
  <transition name="slide-fade">

    <div v-if="showOptions" ref="optionsDropdown" @click.stop :class="isDarkMode ? ' bg-gray-900 text-white' : 'bg-white text-gray-900'" class="dropdown-size absolute right-4 bottom-16 shadow-lg rounded-md p-4">
        <button @click="toggleDarkMode" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
            Dark Mode
            <img v-if="isDarkMode" src="@/assets/moon.png" alt="Moon Icon" class="w-6 h-6" />
            <img v-else src="@/assets/sun.png" alt="Sun Icon" class="w-6 h-6" />
        </button>
        <button @click="logout" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
            Logout
            <font-awesome-icon icon="right-from-bracket" />
        </button>
        <button @click="profile" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
            Profile
            <font-awesome-icon icon="user" />
        </button>
        <button v-if="isAdmin" @click="workers" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
            Workers
            <font-awesome-icon icon="users-gear" />
        </button>
        <button v-if="isAdminOrWorker" @click="clients" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
            Clients
            <font-awesome-icon icon="handshake" />
        </button>
        <button v-if="isAdminOrWorker" @click="productForm" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
          Add product
          <font-awesome-icon icon="plus" />
        </button>
        <button  @click="qrcodes" class="w-full flex items-center justify-between p-4 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
          QRCodes
          <font-awesome-icon icon="qrcode" />
        </button>

    </div>
  </transition>
  


  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted , computed} from 'vue';
import { isDarkMode } from '@/state.js';
import { useRouter } from 'vue-router';
import axios from 'axios';


const router = useRouter();
const showOptions = ref(false);
const optionsButton = ref(null);
const optionsDropdown = ref(null);
const user = ref(null);  // Adding user ref


const cartItems = ref([]);  // This needs to be defined first

onMounted(async () => {
    try {
        const userResponse = await axios.get('http://localhost:5000/user_details');
        if (userResponse.data) {
            user.value = userResponse.data;  // Set the user data
        }


        const response = await axios.get('http://localhost:5000/cart');
        cartItems.value = response.data.cart_items;
    } catch (error) {
        console.error('Failed to fetch cart items:', error);
    }
});

const isAdminOrWorker = computed(() => {
  return user.value && (user.value.role === 'admin' || user.value.role === 'worker');
});

const isAdmin = computed(() => {
  return user.value && (user.value.role === 'admin');
});

const totalCartItems = computed(() => {
    return cartItems.value.reduce((acc, item) => acc + item.quantity, 0);
});

onUnmounted(() => {
  document.removeEventListener("click", outsideClickListener);
});

const outsideClickListener = (event) => {
  if (optionsButton.value && !optionsButton.value.contains(event.target) && 
      optionsDropdown.value && !optionsDropdown.value.contains(event.target)) {
    showOptions.value = false;
  }
};

const toggleOptions = () => {
  showOptions.value = !showOptions.value;
};

const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
    localStorage.setItem('dark-mode', isDarkMode.value);
};

const logout = async () => {
    try {
        const response = await axios.post('http://localhost:5000/logout');
        if (response.data.success) {
            // Handle successful logout
            // For example, you can redirect to the login page or update the UI state to reflect that the user is logged out
            router.push('/'); // Assuming you have a login route
        } else {
            console.error('Failed to logout:', response.data.message);
        }
    } catch (error) {
        console.error('Error during logout:', error);
    }
};


const profile = () => {
  router.push({ name: 'Profile' }); // Assuming the route name for Profile.vue is 'Profile'
};

const workers = () => {
  router.push({ name: 'Workers' }); // Assuming the route name for Profile.vue is 'Profile'
};

const productForm = () => {
  router.push({ name: 'ProductForm' }); 
};

const qrcodes = () => {
  router.push({ name: 'QRCodes' }); 
};





const clients = () => {
  router.push({ name: 'Clients' }); // Assuming the route name for Profile.vue is 'Profile'
};


</script>

  
  <style>
  /* Animation for the icon transition */
  .fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
  }
  
  /* Dark mode styles */
  .dark {
  background-color: #101c31;
  color: #e2e8f0; /* Light gray for main text */
  }
  
  .dark h1, .dark h2, .dark h3, .dark h4, .dark h5, .dark h6 {
  color: #6a8393; /* Slightly brighter color for headings */
  }
  
  .dark a {
  color: #ffffff; /* Subtle blue for links */
  }
  
  /* Navbar styles */
  nav {
  position: relative;
  transition: all 0.5s;
  }
  /* Container to position the icons */
  .icon-container {
    position: relative;
    width: 24px;
    height: 24px;
    perspective: 1000px;
  }
  
  /* styles for the icons */
  .icon {
    width: 32px;
    height: 32px;
    transition: all 0.5s ease;
  }
  
  /* Slide and fade transition */
  .slide-fade-enter-active, .slide-fade-leave-active {
    transition: all 0.5s ease;
  }
  
  .slide-fade-enter, .slide-fade-leave-to /* .slide-fade-leave-active in <2.1.8 */ {
    transform: translateY(-20px);
    opacity: 0;
  }
  
  /* Enhanced Navbar styles */
  nav {
    transition: all 0.5s;
    border-bottom: 4px solid rgba(255, 255, 255, 0.1); /* thicker border for a modern look */
    box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.1); /* subtle shadow for depth */
  }
  
  /* Gradient background for a vibrant look */
  nav {
    background-image: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
  }
  
  /* Logo hover effect for interactivity */
  nav .flex-shrink-0 img:hover {
    transform: scale(1.5);
    transition: transform 0.3s ease;
  }
  
  /* Hover effect for links for better UX */
  nav a:hover {
    text-decoration: none;
    transform: translateY(-2px); /* subtle lift on hover */
  }
  
  /* Button hover effect for better UX */
  nav button:hover {
    transform: translateY(-3px); /* subtle lift on hover */
  }
  
  
  
  /* Enhancing the shadow for a floating effect */
  nav {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border-radius: 30px; /* rounded corners for a modern look */
    margin: 0 16px; /* some margin on the sides for the rounded corners to be visible */
    margin-left: px;
    margin-right: px;
  }
  
  /* Adding a subtle transition for the hover effects */
  nav a, nav button {
    transition: all 0.3s ease;
    margin-left: 10px;
    
  }
.dropdown-size button {
    font-size: 20px;  /* adjust this value to make the font size bigger or smaller */
    padding: 15px 8px;  /* adjust these values to make the padding bigger or smaller */
  }
  /* Slide-fade transition styles */
.slide-fade-enter-active, .slide-fade-leave-active {
    transition: opacity 0.5s, transform 0.5s;
}

.slide-fade-enter, .slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-1em);
}


.nav-z-index {
    z-index: 9998; /* Setting a value just below the dropdown's z-index */
}
  

  </style>
  
  
  