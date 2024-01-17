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
        <h1 class="text-3xl font-bold mb-6">All the Clients</h1>

        <div class="flex justify-end mb-1">
          <router-link 
            to="/register" 
            :class="isDarkMode ? 'text-gray-700' : 'text-white'"
            class="w-20 h-14 flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-purple-500 hover:to-cyan-600 shadow-md hover:shadow-lg rounded-full transform transition-all duration-200 hover:scale-110"
          >
            <font-awesome-icon icon="user-plus"/>
          </router-link>
        </div>

        <!-- Display Clients Table -->
        <div v-if="computedClients.length" class="overflow-hidden rounded-lg shadow-lg">
          <table class="min-w-full leading-normal">
            <thead>
              <tr>
                <th class="py-4  bg-indigo-600 text-white font-bold uppercase text-sm">St</th>
                <th class="py-4  bg-indigo-600 text-white font-bold uppercase text-sm">ID</th>
                <th class="py-4 px-2 bg-indigo-600 text-white font-bold uppercase text-sm">Username</th>
                <th class="py-4  bg-indigo-600 text-white font-bold uppercase text-sm">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client in computedClients" :key="client.id" class="bg-gray-200 dark:bg-gray-800">
                <!-- Status Indicator Column -->
                <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">
                    <span :class="client.statusClass" class="inline-block w-3 h-3 rounded-full"></span>
                </td>

                <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">{{ client.id }}</td>
                <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">{{ client.username }}</td>
                <td class="py-4 px-6 border-b border-gray-200 dark:border-gray-700">
                  <!-- Update and Delete buttons -->
                  <button @click="openUpdateModal(client)" class="mr-2 px-5 py-4 text-white bg-gradient-to-r from-green-500 to-green-700 rounded-full">
                    <font-awesome-icon icon="pen-to-square" />
                  </button>
                  <button @click="deleteClient(client.id)" class=" px-5 py-4 text-white bg-gradient-to-r from-red-600 to-pink-500 rounded-full">
                    <font-awesome-icon icon="trash-can-arrow-up" />
                  </button>

                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          No clients found.
        </div>
      </div>
    </div>


    <!-- Update Client Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 backdrop-blur-md overflow-y-auto h-full w-full flex items-center justify-center" @click.self="closeModal">
      <div class="relative  bg-white dark:bg-gray-800 rounded-lg shadow-xl">
        <!-- Modal Header -->
        <div class="flex justify-between items-center bg-gradient-to-r from-indigo-600 to-blue-700 p-5 rounded-t-lg">
          <h3 class="text-xl text-white font-semibold">Edit Client</h3>
          <button class="bg-red-500 hover:bg-red-700 text-white rounded-full p-1.5 ml-auto inline-flex items-center" @click="closeModal">
            <svg class="w-6 h-6" fill="none" stroke="white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <!-- Modal Body -->
        <div class="p-6">
          <div class="mb-4">
            <label for="username" class="block mb-2 text-sm font-medium text-gray-900">Username:</label>
            <input type="text" id="username" v-model="editableClient.username"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                  placeholder="Enter new username">
          </div>
          <div class="mb-4">
            <label for="password" class="block mb-2 text-sm font-medium text-gray-900">New Password:</label>
            <input type="password" id="password" v-model="editableClient.password"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                  placeholder="Enter new password">
          </div>
          <!-- Modal Footer -->
          <div class="flex flex-col items-center justify-between p-4 space-y-4">
            <div class="flex space-x-4">
              <button @click="activateClient(editableClient.id)" class="px-8 py-3 text-white bg-gradient-to-r from-green-500 to-green-700 rounded-full">
                Activate
              </button>
              <button @click="deactivateClient(editableClient.id)" class="px-6 py- text-white bg-gradient-to-r from-red-600 to-pink-500 rounded-full">
                Deactivate
              </button>
            </div>
            <button @click="saveClientChanges" class="w-full px-5 py-3 text-white bg-blue-700 rounded-full"><font-awesome-icon icon="floppy-disk" />
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';
import { useRoute, useRouter } from 'vue-router';

// Component state
let clients = ref([]);
let notification = ref({ message: '', type: '' });
let showModal = ref(false);
let editableClient = ref({});


onMounted(() => {
  fetchClients();
});


const fetchClients = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/clients');
        console.log("API Response:", response.data); // Log the full response data
        clients.value = response.data.map(client => ({
            ...client,
            isActive: client.isActive ?? false // Fallback to false if undefined
        }));
    } catch (err) {
        console.error("Error fetching clients:", err);
        clients.value = [];
    }
};

const openUpdateModal = (client) => {
  editableClient.value = { ...client };
  showModal.value = true;
};


const closeModal = () => {
  showModal.value = false;
  editableClient.value = {};
};


const updateClient = (client) => {
  editableClient.value = { ...client };
  showModal.value = true;
};


const deleteClient = async (clientId) => {
    try {
        const confirmation = confirm("Are you sure you want to delete this client?");
        if (confirmation) {
            const response = await axios.delete(`http://localhost:5000/api/clients/${clientId}`);
            if (response.data.success) {
                fetchClients(); // Refresh the client list
            } else {
                alert(response.data.message || 'Deletion failed.');
            }
        }
    } catch (err) {
        alert('Error deleting client.');
    }
};

const activateClient = async (clientId) => {
    try {
        const response = await axios.put(`http://localhost:5000/api/clients/${clientId}/activate`);
        if (response.data.success) {
            fetchClients(); // Refresh the client list
        } else {
            alert(response.data.message || 'Activation failed.');
        }
    } catch (err) {
        alert('Error activating client.');
    }
};

const deactivateClient = async (clientId) => {
    try {
        const response = await axios.put(`http://localhost:5000/api/clients/${clientId}/deactivate`);
        if (response.data.success) {
            fetchClients(); // Refresh the client list
        } else {
            alert(response.data.message || 'Deactivation failed.');
        }
    } catch (err) {
        alert('Error deactivating client.');
    }
};

const computedClients = computed(() => {
    return clients.value.map(client => {
        // Determine the status class based on the client's status
        let statusClass = 'bg-gray-500'; // Default to gray
        if (client.status === 'active') {
            statusClass = 'bg-green-500';
        } else if (client.status === 'deactive') {
            statusClass = 'bg-red-500';
        }

        return {
            ...client,
            statusClass
        };
    });
});

const saveClientChanges = async () => {
  if (!editableClient.value.username) {
    // Handle empty username case
    alert('Username cannot be empty');
    return;
  }

  try {
    const response = await axios.put(`http://localhost:5000/api/clients/${editableClient.value.id}`, {
      username: editableClient.value.username,
      password: editableClient.value.password // send password to backend
    });
    if (response.data.success) {
      fetchClients();
      showModal.value = false;
    } else {
      alert(response.data.message || 'Update failed.');
    }
  } catch (err) {
    alert('Error updating client.');
  }
};




onMounted(fetchClients);

</script>

