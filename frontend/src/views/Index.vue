<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">

    <!-- Navbar -->
    <Navbar>Navbar is here!</Navbar>

    <!-- Main content -->
    <div class="py-20">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 text-center">
        <h1 v-if="loggedInUser" class="text-3xl font-semibold text-gray-900 mb-4">Hello, {{ loggedInUser }}, you are logged in successfully!</h1>
        <h1 v-else class="text-3xl font-semibold text-gray-900 mb-4">You don't have access. Please login.</h1>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import { ref } from 'vue';
import { isDarkMode } from '@/state.js';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  components: {
    Navbar
  },
  setup() {
    const loggedInUser = ref('Demo User');
    const router = useRouter();

    const logout = async () => {
        try {
            await axios.post('http://localhost:5000/logout');
            localStorage.removeItem('loggedInUser');
            router.push('/');
        } catch (error) {
            alert('Failed to log out.');
        }
    };

    const fetchUserDetails = async () => {
        try {
            const response = await axios.get('http://localhost:5000/user_details');
            loggedInUser.value = response.data.username;
        } catch (error) {
            if (error.response && error.response.status === 401) {
                // If unauthorized, redirect to login page
                router.push('/');
            } else {
                alert('Failed to fetch user details.');
            }
        }
    };

    // Call the method to fetch user details when the component is loaded
    fetchUserDetails();

    return {
      loggedInUser,
      logout,
      isDarkMode
    };
  }
}
</script>
