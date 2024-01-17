<template>
  <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
    <Navbar />
    <div class="container mx-auto p-4">
      <div v-if="washproduct" class="max-w-xl mx-auto bg-white dark:bg-gray-600 rounded-3xl shadow-lg overflow-hidden">
        <div class="p-4">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ washproduct.name }}</h2>
          <p class="text-gray-700 dark:text-gray-300 mb-4">{{ washproduct.description }}</p>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">Price: ${{ washproduct.price }}</div>
          <div class="mt-4">
            <div v-for="image in washproduct.images" :key="image" class="w-28 mb-4">
              <img :src="'http://localhost:5000/uploads/' + image" alt="Washproduct Image" class="w-full h-auto object-contain">
            </div>
          </div>
          <div class="mt-4">
            <button @click="initiateCheckout" class="mr-14 py-3 px-6 text-white bg-gradient-to-r from-indigo-500 to-sky-500 shadow-md rounded-full">Paguaj </button>
            <button @click="navigateToEditPage" class="mr-2 py-4 px-5 text-white bg-gradient-to-r from-green-500 to-green-700 shadow-md rounded-full"><font-awesome-icon icon="pen-to-square" /></button>
            <button @click="deleteWashproduct" class="py-4 px-5 text-white bg-gradient-to-r from-red-600 to-pink-500 hover:from-pink-600 shadow-md rounded-full"><font-awesome-icon icon="trash-can-arrow-up" /></button>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 dark:text-gray-300">
        <p>Washproduct not found.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { isDarkMode } from '@/state.js';
import { loadStripe } from '@stripe/stripe-js';

const route = useRoute();
const router = useRouter();
const washproduct = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:5000/washproducts/${route.params.id}`);
    washproduct.value = response.data;
  } catch (error) {
    console.error('Error fetching washproduct:', error);
  }
});

const navigateToEditPage = () => {
  router.push(`/washproducts/edit/${washproduct.value.id}`);
};

const deleteWashproduct = async () => {
  if (confirm('Are you sure you want to delete this washproduct?')) {
    try {
      await axios.delete(`http://localhost:5000/washproducts/delete/${washproduct.value.id}`);
      alert('Washproduct deleted successfully');
      router.push('/index');
    } catch (error) {
      console.error('Error deleting washproduct:', error);
      alert('Failed to delete washproduct');
    }
  }
};

const initiateCheckout = async () => {
  if (washproduct.value) {
    try {
      const response = await axios.post('http://localhost:5000/create-washproduct-checkout-session', {
        productId: washproduct.value.id
      });

      if (response.data.sessionId) {
        const stripe = await loadStripe('pk_test_51O5ONQLYq60Cyx2ypbhz9i3Xk572jV1PIaWmrwbx4TIKVqUovuhhVvAjksyMN7hslMFEjdHLs5as5E4sj33ND28b00Puxc7y5m');
        stripe.redirectToCheckout({ sessionId: response.data.sessionId });
      } else {
        console.error('Failed to create Stripe Checkout session');
      }
    } catch (error) {
      console.error('Error initiating Stripe Checkout:', error);
    }
  }
};
</script>
