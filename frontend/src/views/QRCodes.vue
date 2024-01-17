<template>
  <div :class="{ 'dark': isDarkMode }" class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
    <Navbar />

    <div class="container mx-auto p-6">
      <div v-if="qrcodes.length === 0 || qrcodes.every(qr => !qr.is_valid)" class="mt-10 p-10 bg-white dark:bg-gray-700 rounded-3xl shadow-lg mx-auto text-center">
        <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">No Active QR Codes</h2>
        <p class="text-lg text-gray-600 dark:text-gray-300">You have not purchased any washes, or your purchase has expired.</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-10">
        <div v-for="qrcode in qrcodes" :key="qrcode.id" class="bg-white dark:bg-gray-700 rounded-3xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
          <div class="p-6 flex flex-col items-center justify-center">
            <p class="text-lg text-gray-600 dark:text-gray-300 text-center">Thank you for choosing our products, this is your qr code</p>
            <img v-if="qrcode.qr_image" :src="'data:image/png;base64,' + qrcode.qr_image" alt="QR Code" class="w-56 h-56">
            <p :class="{'text-green-500': qrcode.is_valid, 'text-red-500': !qrcode.is_valid, 'text-lg': true, 'font-semibold': true, 'mt-4': true}">
              {{ qrcode.is_valid ? 'Valid QR Code' : 'Expired QR Code' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { isDarkMode } from '@/state.js';
  import Navbar from './Navbar.vue';
  
  const qrcodes = ref([]);
  
  const fetchQRCodes = async () => {
    try {
      const response = await axios.get('http://localhost:5000/user-qrcodes');
      qrcodes.value = response.data;
    } catch (error) {
      console.error('Error fetching QR codes:', error);
    }
  };
  
  const refreshQRCodes = () => {
  setInterval(fetchQRCodes, 300000); // Refresh every 5 minutes (300000 milliseconds)
};

onMounted(() => {
  fetchQRCodes();
  refreshQRCodes();
});  </script>


<style scoped>
.mb-15 {
    margin-bottom: 5.0rem;
}

</style>