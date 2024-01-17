<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">
      <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
          <div>
            <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Register
            </h2>
          </div>
          <form class="mt-8 space-y-6" @submit.prevent="register">
            <div class="rounded-md shadow-sm -space-y-px">
              <div>
                <label for="username" class="sr-only">Username</label>
                <input v-model="username" id="username" name="username" type="text" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Username">
              </div>
              <div>
                <label for="password" class="sr-only">Password</label>
                <input v-model="password" id="password" name="password" type="password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password">
              </div>
              <div>
                  <label for="role" class="sr-only ">Role</label>
                  <select v-model="role" id="role" name="role" required class=" appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm">
                      <option value="client">Client</option>
                      <option v-if="isAdmin" value="worker">Worker</option>
                      <option v-if="isAdmin" value="admin">Admin</option>
                  </select>
              </div>
                
            </div>
            <div>
              <button type="submit" class="group relative w-full flex justify-center border border-transparent text-sm font-medium px-5 py-2 text-white bg-gradient-to-r from-indigo-600 to-blue-900 hover:from-blue-900 hover:to-indigo-600 shadow-md hover:shadow-lg rounded-full transform transition-all hover:scale-110">
                Register
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { isDarkMode } from '@/state.js';  // Import the isDarkMode state

  
  const username = ref('');
  const password = ref('');
  const role = ref('admin');
  const router = useRouter();
  const user = ref(null);  // Adding user ref


  onMounted(async () => {
    try {
        const userResponse = await axios.get('http://localhost:5000/user_details');
        if (userResponse.data) {
            user.value = userResponse.data;  // Set the user data
        }
      } catch (error) {
        console.error('Failed to fetch user:', error);
    }
});

const isAdmin = computed(() => {
  return user.value && (user.value.role === 'admin');
});
  
  const register = async () => {
    try {
      const response = await axios.post('http://localhost:5000/register', {
        username: username.value,
        password: password.value,
        role: role.value
      });
      if (response.data.success) {
        router.push('/');
      } else {
        alert(response.data.message || 'Registration failed.');
      }
    } catch (error) {
      alert('Registration failed. ' + (error.response?.data?.message || ''));
    }
  };
  </script>
  