<template>
  <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen">
    <!-- Navbar -->
    <Navbar></Navbar>
    <!-- Main content -->
    <div>
      <div class="max-w-7xl mx-auto py-10 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-200">Notifications</h2>
          <button v-if="isAdminOrWorker"
            class=  "mr-1 py-3 px-6 text-white bg-gradient-to-r from-indigo-500 to-sky-500 shadow-md rounded-full"
            type="button"
            @click="showAddNotification = !showAddNotification">
            <font-awesome-icon icon="plus" /> Notification
          </button>
        </div>

        <!-- Tab bar for selecting notifications type -->
        <div class="flex space-x-1 bg-indigo-500 rounded-full mb-4 p-1">
          <button
            class="flex-1 py-2 rounded-full text-sm font-medium leading-5 text-white bg-indigo-500  shadow focus:outline-none"
            :class="{'text-white bg-indigo-700 ': currentTab === 'notifications'}"
            @click="currentTab = 'notifications'">
            Auto Notifications
          </button>
          <button
            class="flex-1 py-2 rounded-full text-sm font-medium leading-5 text-white bg-idigo-500 shadow focus:outline-none"
            :class="{'text-white bg-indigo-700': currentTab === 'simpleNotifications'}"
            @click="currentTab = 'simpleNotifications'">
            Added Notification
          </button>
        </div>

        
        <!-- Modal -->
        <div v-if="showAddNotification" class="fixed inset-0 bg-gray-900 bg-opacity-50 backdrop-blur-md overflow-y-auto h-full w-full flex items-center justify-center" @click.self="showAddNotification = false">
          <div class="relative w-sadu bg-white dark:bg-gray-800 rounded-lg shadow-xl" @click.stop>
            <!-- Modal Header -->
            <div class="flex justify-between items-center bg-gradient-to-r from-indigo-600 to-blue-700 p-5 rounded-t-lg">
              <h3 class="text-xl text-white dark:text-gray-200 font-semibold">New Notification</h3>
              <button v-if="isAdminOrWorker" class="bg-red-500 hover:bg-red-700 text-white rounded-full p-1.5 ml-auto inline-flex items-center" @click="showAddNotification = false">
                <svg class="w-6 h-6" fill="none" stroke="white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            <!-- Modal Body -->
            <div class="p-6">
              <div class="mb-4">
                <label for="description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Description:</label>
                <input type="text" id="description" v-model="newNotification.description"
                      class="bg-gray-50 border h-20  border-gray-300 text-gray-900 dark:text-gray-200 dark:bg-gray-600 dark:border-gray-500 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                      placeholder="Enter notification description" required>
              </div>
              <!-- Modal Footer -->
              <div class="flex justify-center pt-4">
                <button @click="addSimpleNotification" class="w-full px-5 py-3 text-white bg-blue-700 hover:bg-blue-800 focus:ring-2 focus:ring-blue-300 rounded-full">
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Notification List -->
        <ul v-if="currentTab === 'notifications'" class="space-y-4 mb-10">
          <li v-for="notification in notifications" :key="notification.id" class="bg-gray-200 dark:bg-gray-700 shadow-md overflow-hidden rounded-3xl px-6 py-4 flex justify-between items-center">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                Action: <span class="font-semibold">{{ notification.action }}</span> - 
                Product Name: <span class="font-semibold">{{ notification.product_name }}</span> - 
                by: <span class="font-semibold">{{ notification.added_by }}</span> - 
                Timestamp: <span class="font-semibold">{{ new Date(notification.timestamp).toLocaleString() }}</span>
              </p>
            </div>
            <button v-if="isAdminOrWorker" @click="deleteNotification(notification.id)" class="ml-4 px-4 py-4 bg-gradient-to-r from-red-600 to-pink-500 text-white rounded-full p-2 flex items-center justify-center transition duration-300 ease-in-out">
              <font-awesome-icon icon="trash-can-arrow-up" />
            </button>
          </li>
        </ul>

        
        <!-- Simple Notifications -->
        
        <ul v-if="currentTab === 'simpleNotifications'" class="space-y-4 mb-10">
          <li v-for="simpleNotification in simpleNotifications" :key="simpleNotification.id" class="bg-gray-200 dark:bg-gray-700 shadow-md overflow-hidden rounded-3xl px-6 py-4 flex justify-between items-center">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                Creator: <span class="font-semibold">{{ simpleNotification.creator }}</span> - 
                Description: <span class="font-semibold">{{ simpleNotification.description }}</span> - 
                Timestamp: <span class="font-semibold">{{ simpleNotification.date }}</span>
              </p>
            </div>
            <button v-if="isAdminOrWorker" @click="deleteSimpleNotification(simpleNotification.id)" class="ml-4 px-4 py-4 bg-gradient-to-r from-red-600 to-pink-500 text-white rounded-full p-2 flex items-center justify-center transition duration-300 ease-in-out">
              <font-awesome-icon icon="trash-can-arrow-up" />
            </button>
          </li>
        </ul>
        <button v-if="moreNotificationsAvailable && currentTab === 'notifications'"
                @click="loadMoreNotifications"
                class="load-more-btn text-white bg-indigo-500 py-3 px-6 rounded-full m-auto block mb-15">
          Load More Notifications
        </button>

        <button v-if="moreSimpleNotificationsAvailable && currentTab === 'simpleNotifications'"
                @click="loadMoreSimpleNotifications"
                class="load-more-btn text-white bg-indigo-500 py-3 px-6 rounded-full m-auto block mb-15">
          Load More Notifications
        </button>

      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';

// Refs for your data
const user = ref(null);
const notifications = ref([]);
const simpleNotifications = ref([]);
const showAddNotification = ref(false);
const newNotification = ref({ creator: '', description: '' });
const currentTab = ref('notifications');
const notificationsStart = ref(0);
const notificationsLimit = ref(10);  // set your desired limit
const moreNotificationsAvailable = ref(true);
const simpleNotificationsStart = ref(0);
const simpleNotificationsLimit = ref(10); // Set your desired limit
const moreSimpleNotificationsAvailable = ref(true);



// Fetching user and notifications data
onMounted(async () => {
  try {
    const userResponse = await axios.get('http://localhost:5000/user_details');
    if (userResponse.data) {
      user.value = userResponse.data;
      console.log("Fetched User:", user.value); // Debugging line
    }
    await fetchNotifications();
    await fetchSimpleNotifications();

  } catch (error) {
    console.error('Failed to fetch user details or notifications:', error);
  }
});

// Computed property to check admin role
const isAdminOrWorker = computed(() => {
  return user.value && (user.value.role === 'admin' || user.value.role === 'worker');
});

const fetchNotifications = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/notifications`, {
      params: { start: notificationsStart.value, limit: notificationsLimit.value }
    });
    const newNotifications = response.data.filter(
      newNotification => !notifications.value.some(existingNotification => existingNotification.id === newNotification.id)
    );
    notifications.value = [...notifications.value, ...newNotifications];
    moreNotificationsAvailable.value = newNotifications.length === notificationsLimit.value;
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
};





const fetchSimpleNotifications = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/simple-notifications', {
      params: { start: simpleNotificationsStart.value, limit: simpleNotificationsLimit.value }
    });
    const newSimpleNotifications = response.data.filter(
      newNotification => !simpleNotifications.value.some(existingNotification => existingNotification.id === newNotification.id)
    );
    simpleNotifications.value = [...simpleNotifications.value, ...newSimpleNotifications];
    moreSimpleNotificationsAvailable.value = newSimpleNotifications.length === simpleNotificationsLimit.value;
  } catch (error) {
    console.error('Error fetching simple notifications:', error);
  }
};


const addSimpleNotification = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/simple-notifications', {
      description: newNotification.value.description
    });
    simpleNotifications.value.unshift(response.data); // Add to the beginning of the array
    simpleNotifications.value.sort((a, b) => new Date(b.date) - new Date(a.date)); // Re-sort after adding
    newNotification.value = { description: '' };
    showAddNotification.value = false;
  } catch (error) {
    console.error('Error adding simple notification:', error);
  }
};

const deleteNotification = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/api/notifications/${id}`);
    notifications.value = notifications.value.filter(n => n.id !== id);
  } catch (error) {
    console.error('error deleting notifications:', error);
  }
};

const deleteSimpleNotification = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/api/simple-notifications/${id}`);
    simpleNotifications.value = simpleNotifications.value.filter(notification => notification.id !== id);
  } catch (error) {
    console.error('Error deleting simple notification:', error);
  }
};

const loadMoreNotifications = async () => {
  notificationsStart.value += notificationsLimit.value;
  await fetchNotifications();
};

const loadMoreSimpleNotifications = async () => {
  simpleNotificationsStart.value += simpleNotificationsLimit.value;
  await fetchSimpleNotifications();
};


</script>


<style scoped>
.mb-25 {
  margin-bottom: 6rem; /* 80px */
}

.w-sadu {
    width: 88.333333%;
}
.mb-15 {
    margin-bottom: 4rem/* 48px */;
}

</style>
