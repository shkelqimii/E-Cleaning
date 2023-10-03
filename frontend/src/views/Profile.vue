<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">
    
    <!-- Navbar -->
    <Navbar>Navbar is here!</Navbar>
    
    <div class="container mx-auto px-4 py-12">
      <!-- User Info -->
      <div v-if="user" class="bg-sky-100 dark:bg-gray-800 shadow-md rounded-lg p-6 mb-8">
        <h1 class="text-xl font-semibold mb-4">Pour Profile</h1>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Role:</strong> {{ user.role }}</p>
      </div>

      <!-- Change Password -->
      <div class="bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-6">
        <h1 class="text-xl font-semibold mb-4">Change Password:</h1>
        <form @submit.prevent="changePassword">
          <!-- Old Password Input -->
          <div class="mb-4">
            <label for="oldPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Old Password</label>
            <input v-model="oldPassword" type="password" id="oldPassword" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 dark:text-white">
          </div>
          
          <!-- New Password Input -->
          <div class="mb-4">
            <label for="newPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300">New Password</label>
            <input v-model="newPassword" type="password" id="newPassword" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 dark:text-white">
          </div>

          <!-- Confirm New Password Input -->
          <div class="mb-4">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirm New Password</label>
            <input v-model="confirmPassword" type="password" id="confirmPassword" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 dark:text-white">
          </div>

          <button type="submit" class="mr-4 px-32 py-3 text-white bg-gradient-to-r from-green-500 to-green-800 hover:from-yellow-800 hover:to-yellow-400 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { isDarkMode } from '@/state.js';

const user = ref(null);
const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

onMounted(async () => {
    try {
        const response = await axios.get('http://localhost:5000/user_details');
        if (response.data) {
            user.value = response.data;
        }
    } catch (error) {
        console.error('Failed to fetch user details:', error);
    }
});

const changePassword = async () => {
    if (newPassword.value !== confirmPassword.value) {
        alert('Passwords do not match.');
        return;
    }
    try {
        const dataToSend = { 
            old_password: oldPassword.value, 
            new_password: newPassword.value 
        };
        const response = await axios.post('http://localhost:5000/change_password', dataToSend);
        
        if (response.data.success) {
            alert('Password changed successfully!');
            oldPassword.value = '';
            newPassword.value = '';
            confirmPassword.value = '';
        } else {
            alert(response.data.message || 'Failed to change password.');
        }
    } catch (error) {
        alert('Error changing password.');
    }
};
</script>

<style>
/* Add your styles here */
</style>
