<template>
    <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen  dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      <Navbar />
      <div class="p-5">
        <h2 class="text-2xl font-bold mb-7 bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4">Add New Washproduct</h2>
        <form @submit.prevent="submitForm" class="space-y-4 bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4">
          <div>
            <label for="name" class="block text-sm font-medium">Name:</label>
            <input v-model="washproduct.name" id="name" type="text" required class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4">
          </div>
          <div>
            <label for="price" class="block text-sm font-medium">Price:</label>
            <input v-model.number="washproduct.price" id="price" type="number" required class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4">
          </div>
          <div>
            <label for="description" class="block text-sm font-medium">Description:</label>
            <textarea v-model="washproduct.description" id="description" class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-4"></textarea>
          </div>
          <div>
            <label for="images" class="block text-sm font-medium">Images:</label>
            <input type="file" ref="images" multiple required class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-6">
          </div>
          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit</button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue';
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  import { isDarkMode } from '@/state.js';
  
  const washproduct = reactive({
    name: '',
    price: 0,
    description: ''
  });
  const images = ref(null);
  
  const submitForm = async () => {
    const formData = new FormData();
    formData.append('name', washproduct.name);
    formData.append('price', washproduct.price);
    formData.append('description', washproduct.description);
  
    // Append images to formData
    const imageFiles = images.value.files;
    for (let i = 0; i < imageFiles.length; i++) {
      formData.append('images', imageFiles[i]);
    }
  
    try {
      const response = await axios.post('http://localhost:5000/washproducts/add', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
  
      if (response.status === 201) {
        alert('Washproduct added successfully');
        // Reset form after successful submission
        washproduct.name = '';
        washproduct.price = 0;
        washproduct.description = '';
      }
    } catch (error) {
      console.error('Error adding washproduct:', error);
      alert('Failed to add washproduct');
    }
  };
  </script>
  
  
  <style scoped>
  /* Additional custom styles if needed */
  </style>
  