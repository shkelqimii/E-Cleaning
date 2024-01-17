<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen font-sans">
      <Navbar />
  
      <div class="container mx-auto px-4 py-10">
        <h2 class="text-2xl font-bold mb-7 bg-gray-200 dark:bg-gray-800 shadow-md rounded-lg p-4">Edit Washproduct</h2>
        <form @submit.prevent="updateWashproduct">
          <!-- Name Field -->
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium mb-2">Washproduct Name:</label>
            <input v-model="washproduct.name" type="text" id="name" class="border rounded w-full py-2 px-3 dark:bg-gray-700">
          </div>
  
          <!-- Price Field -->
          <div class="mb-4">
            <label for="price" class="block text-sm font-medium mb-2">Washproduct Price:</label>
            <input v-model="washproduct.price" type="number" step="0.01" id="price" class="border rounded w-full py-2 px-3 dark:bg-gray-700">
          </div>
  
          <!-- Description Field -->
          <div class="mb-4">
            <label for="description" class="block text-sm font-medium mb-2">Washproduct Description:</label>
            <textarea v-model="washproduct.description" id="description" rows="4" class="border rounded w-full py-2 px-3 dark:bg-gray-700"></textarea>
          </div>
  
          <!-- Images Section -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Images:</label>
            <div v-for="(image, index) in washproduct.images" :key="index" class="mb-2">
              <img :src="'http://localhost:5000/uploads/' + image" alt="Washproduct Image" class="w-32 h-32 object-contain">
              <button type="button" @click="removeImage(index)">Remove</button>
            </div>
            <input type="file" ref="newImages" multiple class="mt-1 p-2 w-full border rounded-md dark:bg-gray-700 mb-6">
          </div>
  
          <button type="submit" class="bg-indigo-600 text-white py-4 px-6 rounded-full mb-12">Save Changes</button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import Navbar from './Navbar.vue';
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import axios from 'axios';
  import { isDarkMode } from '@/state.js';
  
  const router = useRouter();
  const route = useRoute();
  const washproduct = ref({ name: '', price: 0, description: '', images: [] });
  const newImages = ref(null);
  
  onMounted(async () => {
    try {
      const response = await axios.get(`http://localhost:5000/washproducts/${route.params.id}`);
      washproduct.value = response.data;
    } catch (error) {
      console.error('Error fetching washproduct:', error);
    }
  });
  
  const updateWashproduct = async () => {
    const formData = new FormData();
    formData.append('name', washproduct.value.name);
    formData.append('price', washproduct.value.price);
    formData.append('description', washproduct.value.description);
  
    // Append new images to formData
    if (newImages.value && newImages.value.files) {
      for (let i = 0; i < newImages.value.files.length; i++) {
        formData.append('images', newImages.value.files[i]);
      }
    }
  
    try {
      await axios.put(`http://localhost:5000/washproducts/edit/${washproduct.value.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      router.push('/index');
    } catch (error) {
      console.error('Error updating washproduct:', error);
    }
  };
  
  const removeImage = (index) => {
    washproduct.value.images.splice(index, 1);
  };
  </script>
  
  <style scoped>
  /* Your existing styles */
  </style>
  