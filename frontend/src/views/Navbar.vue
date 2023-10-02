<template>
  <nav :class="isDarkMode ? 'bg-gradient-to-r from-violet-900 to-blue-900' : 'bg-gradient-to-r from-violet-300 to-blue-300'" class="shadow-lg transition-all duration-500 fixed bottom-0 w-full flex justify-center items-center p-1 mx-auto ">
      
      <!-- Center: Home Link -->
      <router-link 
          to="/index" 
          :class="isDarkMode ? 'text-gray-700' : 'text-white'"
          class="w-16 h-16 flex items-center justify-center bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110"
      >
          <font-awesome-icon icon="house" class="text-xl" />
      </router-link>

      <!-- Right: Options Button (positioned absolutely) -->
      <button @click="showOptions = !showOptions" class="w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110 absolute right-4 bottom-2">
          <font-awesome-icon icon="gear" class="text-xl text-white" />
      </button>


      <!-- Dropdown with Logout and Dark Mode Toggle -->
      <div v-if="showOptions" :class="isDarkMode ? 'bg-gray-800 text-white' : 'bg-white text-gray-900'" class="absolute right-4 bottom-16 shadow-lg rounded-md p-2">
          <button @click="toggleDarkMode" class="w-full flex items-center justify-between p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
              Dark Mode
              <img v-if="isDarkMode" src="@/assets/moon.png" alt="Moon Icon" class="w-6 h-6" />
              <img v-else src="@/assets/sun.png" alt="Sun Icon" class="w-6 h-6" />
          </button>
          <button @click="logout" class="w-full flex items-center justify-between p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
              Logout
              <font-awesome-icon icon="right-from-bracket" />
          </button>
          <button @click="profile" class="w-full flex items-center justify-between p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md">
              profile
              <font-awesome-icon icon="user" />
          </button>
          

      </div>
  </nav>
</template>


  
<script setup>
import { ref } from 'vue';
import { isDarkMode } from '@/state.js';
import { useRouter } from 'vue-router';

const router = useRouter();
const showOptions = ref(false);  // New ref to track dropdown visibility

const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
    localStorage.setItem('dark-mode', isDarkMode.value);
};

const logout = () => {
    localStorage.removeItem('loggedInUser');
    router.push('/');
};
const profile = () => {
  router.push({ name: 'Profile' }); // Assuming the route name for Profile.vue is 'Profile'
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
  </style>
  
  
  
  