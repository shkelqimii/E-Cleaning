<template>
  <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
    <!-- Navbar -->
    <Navbar>Navbar is here!</Navbar>

    <!-- Main content -->
    <div class="py-7">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 text-center">
        <h1 v-if="loggedInUser" class="text-2xl font-semibold text-gray-900 mb-4">
          Hello, {{ loggedInUser }}, you are logged in successfully😀
        </h1>
        <h1 v-else class="text-3xl font-semibold text-gray-900 mb-4">
          You don't have access. Please login.
        </h1>
      </div>
    </div>

    <!-- Washproducts List -->
    <div class="">
      <h2 class="text-xl mb-4">Types of Washs</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="washproduct in washproducts"
          :key="washproduct.id"
          class="bg-white dark:bg-gray-400 rounded-3xl overflow-hidden shadow-md duration-300 ease-in-out flex items-center justify-between"
          @click="navigateToWashproductDetail(washproduct.id)"
        >
          <!-- Washproduct Content -->
          <div class="flex-grow p-4">
            <!-- Washproduct Name -->
            <div class="product-name text-lg block mb-1 hover:text-blue-600 dark:text-gray-700 transition-colors duration-300 ease-in-out">
              {{ washproduct.name }}
            </div>

            <!-- Washproduct Price -->
            <p class="product-price text-lg text-gray-700 dark:text-gray-700 border-t border-b py-1 border-gray-300 dark:border-gray-700 inline-block font-bold">
              {{ washproduct.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}€
            </p>
          </div>

          <!-- Washproduct Image -->
          <div v-if="washproduct.images && washproduct.images.length > 0" class="w-16 h-16 mr-4">
            <img :src="'http://localhost:5000/uploads/' + washproduct.images[0]" alt="Washproduct Image" class="w-full h-full object-contain rounded">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { isDarkMode } from '@/state.js';
import Navbar from './Navbar.vue';

const loggedInUser = ref('Demo User');
const router = useRouter();
const washproducts = ref([]);

const fetchUserDetails = async () => {
  try {
    const response = await axios.get('http://localhost:5000/user_details');
    loggedInUser.value = response.data.username;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push('/');
    } else {
      console.error('Error fetching user details:', error);
    }
  }
};

const fetchWashproducts = async () => {
  try {
    const response = await axios.get('http://localhost:5000/washproducts');
    washproducts.value = response.data;
  } catch (error) {
    console.error('Error fetching washproducts:', error);
  }
};

const navigateToWashproductDetail = (id) => {
  router.push(`/washproducts/${id}`);
};

onMounted(() => {
  fetchUserDetails();
  fetchWashproducts();
});
</script>
