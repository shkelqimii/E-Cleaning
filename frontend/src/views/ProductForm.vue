<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen ">
    <!-- Navbar -->
    <Navbar />
      <div class="p-5">
        <h2 class="text-2xl font-bold mb-7 bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4  ">Add New Product</h2>
        <form @submit.prevent="addProduct" class="space-y-4">

            <div class="bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4  ">
              <div >
                <label for="name" class="block text-sm font-medium ">Name:</label>
                <input v-model="name" id="name" type="text" required class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4">
              </div>
        
              <div>
                <label for="price" class="block text-sm font-medium ">Price:</label>
                <input v-model="formattedPrice" @blur="formatPrice" @input="formatPriceOnInput" id="price" type="text" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4">
              </div>

        
              <div>
                <label for="description" class="block text-sm font-medium ">Description:</label>
                <textarea v-model="description" id="description" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4"></textarea>
              </div>

              <div>
                <label for="quantity" class="block text-sm font-medium " >Qauantity</label>
                <input v-model.number="quantity" id="quantity" type="number" required min="0" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4">
              </div>
        
              <div>
                <label class="block text-sm font-medium  ">Images:</label>
                <input type="file" ref="images" multiple required class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-6">
              </div>
        
              <button type="submit" class="bg-indigo-600 text-white py-4 px-6 rounded-full ">Add Product</button>
            </div>

        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  import { isDarkMode } from '@/state.js';
  
  const name = ref('');
  const price = ref('');
  const description = ref('');
  const quantity = ref(0);
  const images = ref(null);
  const formattedPrice = ref('');
  
  const addProduct = async () => {
    const formData = new FormData();
    formData.append('name', name.value);
    formData.append('price', price.value);
    formData.append('description', description.value);
    formData.append('quantity', quantity.value);
    const imageFiles = images.value.files;
    for (let i = 0; i < imageFiles.length; i++) {
      formData.append('images', imageFiles[i]);
    }
  
    try {
      const response = await axios.post('http://localhost:5000/add_product', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      if (response.data.success) {
        alert('Product added successfully!');
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      alert('Failed to add product.');
    }
  };

  const formatPriceOnInput = (event) => {
  const value = event.target.value.replace(/[^\d.]/g, '');
  price.value = parseFloat(value);
  formattedPrice.value = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' }).format(value);
};

const formatPrice = () => {
  formattedPrice.value = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' }).format(price.value);
};

// Call formatPrice initially if you want the default value to be formatted
formatPrice();
  </script>
  