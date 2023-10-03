<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">
      <!-- Navbar -->
      <Navbar />
  
      <!-- Flash Notification -->
      <transition name="fade" mode="out-in">
          <div v-if="notification.message" :class="`notification ${notification.type}`">
              {{ notification.message }}
          </div>
      </transition>
    
      <!-- Main content -->
      <div class="py-4">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 text-center">
           <!-- Add new User button -->
           <h1 class="text-3xl font-bold mb-6">All the Workers</h1>

         <div class="flex justify-end mb-1">
      <router-link 
          to="/register" 
          :class="isDarkMode ? 'text-gray-700' : 'text-white'"
          class="w-20 h-14 flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-purple-500 hover:to-cyan-600 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110"
      >
      <font-awesome-icon icon="user-plus"/>
      </router-link>
    </div>
          <!-- Display Workers Table -->
          <div v-if="workers.length" class="overflow-hidden rounded-lg shadow-lg">
            <table class="min-w-full leading-normal">
              <thead>
                <tr>
                  <th class="py-4 px-6 bg-indigo-600 text-white font-bold uppercase text-sm">ID</th>
                  <th class="py-4 px-6 bg-indigo-600 text-white font-bold uppercase text-sm">Username</th>
                  <th class="py-4 px-6 bg-indigo-600 text-white font-bold uppercase text-sm">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="worker in workers" :key="worker.id" class="bg-gray-200 dark:bg-gray-800">
                  <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">{{ worker.id }}</td>
                  <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">{{ worker.username }}</td>
                  <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">
                      <button @click="updateWorker(worker.id)" class="mr-2 px-5 py-4 text-white bg-gradient-to-r from-green-500 to-green-700 hover:from-yellow-700 hover:to-yellow-400 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110"><font-awesome-icon icon="pen-to-square" /></button>
                      <button @click="deleteWorker(worker.id)" class=" px-5 py-4 text-white bg-gradient-to-r from-red-600 to-pink-500 hover:from-pink-600 hover:to-red-800 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110"><font-awesome-icon icon="trash-can-arrow-up" /></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            No workers found.
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  import { isDarkMode } from '@/state.js';
  
  let workers = ref([]);
  let notification = ref({ message: '', type: '' });
  
  const fetchWorkers = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/workers');
      workers.value = response.data;
    } catch (err) {
      console.error("Error fetching workers:", err);
      workers.value = [];
    }
  };
  
  const updateWorker = async (workerId) => {
    try {
        const updatedUsername = prompt("Enter new username:");
        if (updatedUsername) {
            const response = await axios.put(`http://127.0.0.1:5000/api/workers/${workerId}`, { username: updatedUsername });
            if (response.data.success) {
                fetchWorkers(); // Refresh the worker list
            } else {
                alert(response.data.message || 'Update failed.');
            }
        }
    } catch (err) {
        alert('Error updating worker.');
    }
};


const deleteWorker = async (workerId) => {
    try {
        const confirmation = confirm("Are you sure you want to delete this worker?");
        if (confirmation) {
            const response = await axios.delete(`http://127.0.0.1:5000/api/workers/${workerId}`);
            if (response.data.success) {
                fetchWorkers(); // Refresh the worker list
            } else {
                alert(response.data.message || 'Deletion failed.');
            }
        }
    } catch (err) {
        alert('Error deleting worker.');
    }
};


  
  fetchWorkers();
  </script>
  
  <style>
  /* Your styles for dark mode and other components */
  
  .notification {
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      padding: 10px 20px;
      border-radius: 5px;
      z-index: 1000;
      font-weight: bold;
  }
  
  .notification.success {
      background-color: #48BB78;
      color: white;
  }
  
  .notification.error {
      background-color: #E53E3E;
      color: white;
  }
  
  .fade-enter-active, .fade-leave-active {
      transition: opacity 0.5s;
  }
  
  .fade-enter, .fade-leave-to {
      opacity: 0;
  }
  </style>
  