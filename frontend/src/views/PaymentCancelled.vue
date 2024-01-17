<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen flex flex-col items-center justify-center">
      <!-- Navbar -->
      <Navbar />

      <!-- Payment Cancelled Message -->
      <div class="text-center p-10 bg-white dark:bg-gray-800 rounded-xl shadow-md max-w-md mx-auto">
          <span class="text-6xl">🤖</span>
          <h1 class="text-4xl font-bold mt-4 mb-2 text-red-600 dark:text-red-400">Payment Cancelled</h1>
          <p class="text-lg text-gray-600 dark:text-gray-300">
              Your payment was cancelled. If you faced any issues, please contact support.
          </p>
      </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';
</script>

<style scoped>
/* Additional styles can be added here if needed */
</style>
