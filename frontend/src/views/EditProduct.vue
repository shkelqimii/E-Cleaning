<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen font-sans">
    <!-- Navbar -->
    <Navbar />

    <!-- Product Edit Form -->
    <div class="container mx-auto px-4 py-10">
      <h2 class="text-2xl font-bold mb-7 bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4 ">Edit Product</h2>
      <form @submit.prevent="updateProduct">
        <div class="bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4  ">
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium mb-2">Product Name:</label>
            <input v-model="product.name" type="text" id="name" class="border rounded w-full py-2 px-3 dark:bg-gray-700">
          </div>

          <div class="mb-4">
            <label for="price" class="block text-sm font-medium mb-2">Product Price:</label>
            <input v-model.number="product.price" type="number" step="0.01" id="price" class="border rounded w-full py-2 px-3 dark:bg-gray-700">
            <div v-if="product.original_price" class="mt-2">
              <span class="text-sm">Original Price: {{ product.original_price.toFixed(2) }}€</span><br>
              <span class="text-sm">Discount: {{ discountPercentage }}%</span>
            </div>
          </div>

          <div class="mb-4">
            <label for="description" class="block text-sm font-medium mb-2">Product Description:</label>
            <textarea v-model="product.description" id="description" rows="4" class="border rounded w-full py-2 px-3 dark:bg-gray-700"></textarea>
          </div>

          <div class="mb-4">
            <label for="quantity" class="block text-sm font-medium mb-2">Product Quantity:</label>
            <input v-model.number="product.quantity" type="number" id="quantity" class="border rounded w-full py-2 px-3 dark:bg-gray-700 mb-4">
          </div>

          <button type="submit" class="bg-indigo-600 text-white py-4 px-6 rounded-full ">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { isDarkMode } from '@/state.js';

const router = useRouter();
const route = useRoute();
const product = ref({});

const discountPercentage = computed(() => {
  if (product.value.original_price && product.value.price) {
    return ((1 - (product.value.price / product.value.original_price)) * 100).toFixed(2);
  }
  return '0.00';
});

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:5000/product/${route.params.id}`);
    product.value = response.data;
  } catch (error) {
    console.error('Failed to fetch product details:', error);
  }
});

const updateProduct = async () => {
  try {
    const productData = {
      name: product.value.name,
      price: product.value.price,
      description: product.value.description,
      quantity: product.value.quantity
    };

    console.log("Sending data:", productData);  // Log the data being sent

    const response = await axios.put(`http://localhost:5000/product/${product.value.id}`, productData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.data.success) {
      // If the backend sends back the updated product data including the discount percentage
      product.value = { ...product.value, ...response.data.product };
    }

    router.go();  // Refresh the current route
  } catch (error) {
    console.error('Failed to update product:', error);
  }
};
</script>


<style scoped>
.container {
  max-width: 1280px;
}
/* Additional styling if needed */
</style>
