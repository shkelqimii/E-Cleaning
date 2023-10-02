<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">

      <!-- Navbar -->
      <Navbar>Navbar is here!</Navbar>

      <!-- Main content -->
      <div class="py-20">
          <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 text-center">
              <h1 v-if="user" class="text-3xl font-semibold text-gray-900 mb-4">Username: {{ user.username }}</h1>
              <h2 class="text-xl mt-4">Role: {{ user.role }}</h2>

              <!-- Password Change Section -->
              <div class="mt-8">
                  <h2>Change Password</h2>
                  <div class="flex flex-col items-center justify-center space-y-4">
                      <input v-model="oldPassword" type="password" placeholder="Old Password" class="border p-2 rounded-md">
                      <input v-model="newPassword" type="password" placeholder="New Password" class="border p-2 rounded-md">
                      <button @click="changePassword" class="group relative w-full flex justify-center border border-transparent text-sm font-medium px-5 py-2 text-white bg-gradient-to-r from-indigo-600 to-blue-900 hover:from-blue-900 hover:to-indigo-600 shadow-md hover:shadow-lg rounded-full transform transition-all hover:scale-110">Change Password</button>
                      <p>{{ message }}</p>
                  </div>
              </div>

             
          </div>
      </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref } from 'vue';
import axios from 'axios';
import { isDarkMode } from '@/state.js';  // Ensure this import path is correct

const newPassword = ref('');
const confirmPassword = ref('');

const changePassword = async () => {
    if (newPassword.value !== confirmPassword.value) {
        alert('Passwords do not match.');
        return;
    }

    try {
        const response = await axios.post('http://localhost:5000/change_password', {
            newPassword: newPassword.value
        });

        if (response.data.success) {
            alert('Password changed successfully.');
        } else {
            alert(response.data.message || 'Failed to change password.');
        }
    } catch (error) {
        alert('Error changing password.');
    }
};

const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
};
</script>


<style scoped>
  /* Add any additional styling you need here */
</style>
