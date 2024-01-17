<template>
  <div :class="[isDarkMode ? 'dark' : '', 'transition-all duration-500 min-h-screen']">
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
        <!-- Add new Worker button -->
        <h1 class="text-3xl font-bold mb-6">All the Workers</h1>
        <div class="flex justify-end mb-1">
          <router-link to="/register" :class="[isDarkMode ? 'text-gray-700' : 'text-white', 'w-20 h-14 flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-purple-500 hover:to-cyan-600 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110']">
            <font-awesome-icon icon="user-plus" />
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
                  <button @click="openWorkerModal(worker)" class="mr-2 px-5 py-4 text-white bg-gradient-to-r from-green-500 to-green-700 rounded-full">
                    <font-awesome-icon icon="pen-to-square" />
                  </button>
                  <button @click="deleteWorker(worker.id)" class="px-5 py-4 text-white bg-gradient-to-r from-red-600 to-pink-500 rounded-full">
                    <font-awesome-icon icon="trash-can-arrow-up" />
                  </button>
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

    <!-- Update Worker Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 backdrop-blur-md overflow-y-auto h-full w-full flex items-center justify-center" @click.self="closeModal">
      <div class="relative w-sadu bg-white dark:bg-gray-800 rounded-lg shadow-xl">
        <!-- Modal Header -->
        <div class="flex justify-between items-center bg-gradient-to-r from-indigo-600 to-blue-700 p-5 rounded-t-lg">
          <h3 class="text-xl text-white font-semibold">Edit Worker</h3>
          <button class="bg-red-500 hover:bg-red-700 text-white rounded-full p-1.5 ml-auto inline-flex items-center" @click="closeModal">
            <svg class="w-6 h-6" fill="none" stroke="white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <!-- Modal Body -->
        <div class="p-6">
          <div class="mb-4">
            <label for="username" class="block mb-2 text-sm font-medium text-gray-900">Username:</label>
            <input type="text" id="username" v-model="editableWorker.username"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                  placeholder="Enter new username">
          </div>
          <div class="mb-4">
            <label for="password" class="block mb-2 text-sm font-medium text-gray-900">New Password:</label>
            <input type="password" id="password" v-model="editableWorker.password"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 "
                  placeholder="Enter new password">
          </div>
          <!-- Modal Footer -->
          <div class="flex justify-center p-6 ">
            <button @click="saveWorkerChanges" class="w-full px-5 py-3 bg-blue-600 text-white rounded-full"><font-awesome-icon icon="floppy-disk" />  Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


  
<script setup>
import axios from 'axios';
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';
import { ref } from 'vue'; // Only import ref once

let showModal = ref(false);
let editableWorker = ref({});
let notification = ref({ message: '', type: '' });
let workers = ref([]); // Assuming you have workers ref as well since it's used in the template

const fetchWorkers = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/workers');
    workers.value = response.data;
  } catch (err) {
    notification.value = { message: 'Error fetching workers', type: 'error' };
    console.error("Error fetching workers:", err);
    workers.value = [];
  }
};


const closeModal = () => {
  showModal.value = false;
  editableWorker.value = {};
};

const openWorkerModal = (worker) => {
  editableWorker.value = { ...worker };
  showModal.value = true;
};


const saveWorkerChanges = async () => {
  if (!editableWorker.value.username || !editableWorker.value.password) {
    notification.value = { message: 'Username and password cannot be empty', type: 'error' };
    return;
  }

  try {
    const response = await axios.put(`http://localhost:5000/api/workers/${editableWorker.value.id}`, {
      username: editableWorker.value.username,
      password: editableWorker.value.password
    });

    if (response.data.success) {
      // Close the modal and clear the editableWorker ref
      showModal.value = false;
      editableWorker.value = {};
      notification.value = { message: 'Worker updated successfully', type: 'success' };
      // Refresh the worker list here if necessary
    } else {
      notification.value = { message: response.data.message || 'Update failed', type: 'error' };
    }
  } catch (err) {
    notification.value = { message: 'Error updating worker', type: 'error' };
    console.error("Error updating worker:", err);
  }
};

const deleteWorker = async (workerId) => {
  const confirmation = confirm("Are you sure you want to delete this worker?");
  if (confirmation) {
    try {
      const response = await axios.delete(`http://localhost:5000/api/workers/${workerId}`);
      if (response.data.success) {
        fetchWorkers(); // Refresh the worker list
      } else {
        notification.value = { message: response.data.message || 'Deletion failed.', type: 'error' };
      }
    } catch (err) {
      notification.value = { message: 'Error deleting worker', type: 'error' };
      console.error("Error deleting worker:", err);
    }
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

  .w-sadu {
    width: 88.333333%;
}
  </style>
  