<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">
      <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
          <div>
            <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Login
            </h2>
          </div>
          <form @submit.prevent="login" class="mt-8 space-y-6">
            <div class="rounded-md shadow-sm -space-y-px">
              <div>
                <label for="username" class="sr-only">Username</label>
                <input v-model="username" name="username" type="text" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Username">
              </div>
              <div>
                <label for="password" class="sr-only">Password</label>
                <input v-model="password" name="password" type="password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password">
              </div>
            </div>
            <div>
              <button type="submit" class="group relative w-full flex justify-center border border-transparent text-sm font-medium  px-5 py-2 text-white bg-gradient-to-r from-indigo-600 to-blue-900 hover:from-blue-900 hover:to-indigo-600 shadow-md hover:shadow-lg rounded-full transform transition-all hover:scale-110">
                Login
              </button>
            </div>
            <div class="text-center mt-4">
              <p class="text-gray-600">Forget your password? <router-link to="/register" class="text-indigo-700 hover:text-indigo-500">change</router-link></p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { isDarkMode } from '@/state.js';  // Import the isDarkMode state

  
  const username = ref('');
  const password = ref('');
  const router = useRouter();
  
  const login = async () => {
    try {
      const response = await axios.post('http://localhost:5000/login', {
          username: username.value,
          password: password.value
      }, { withCredentials: true });

        if (response.data.success) {
            localStorage.setItem('authToken', response.data.token);  // Assuming the token is sent with the key 'token'
            router.push('/index');
        } else {
            alert(response.data.message);
        }
    } catch (error) {
        alert('Login failed.');
    }
};


  </script>
  