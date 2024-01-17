<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen flex flex-col items-center justify-center">
        <!-- Navbar -->
        <Navbar />

        <!-- Payment Success Message -->
        <div class="text-center p-10 bg-white dark:bg-gray-800 rounded-xl shadow-md max-w-md mx-auto mb-40">
            <span class="text-6xl">😊</span>
            <h1 class="text-4xl font-bold mt-4 mb-2 text-green-600 dark:text-green-400">Payment Successful!</h1>
            <p class="text-lg text-gray-600 dark:text-gray-300">Your payment has been processed successfully.</p>
        </div>
    </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';
import { onMounted } from 'vue';
import axios from 'axios';

onMounted(async () => {
    try {
        await axios.delete('http://localhost:5000/cart/clear');
    } catch (error) {
        console.error('Error clearing cart:', error);
    }
});
</script>

<style scoped>
/* Additional styles can be added here if needed */
</style>
