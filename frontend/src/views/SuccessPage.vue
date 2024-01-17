<template>
  <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
    <Navbar />
    <div class="container mx-auto p-6">
      <div class="max-w-md mx-auto bg-white rounded-3xl overflow-hidden shadow-md">
        <div class="p-4">
          <h2 v-if="isValid" class="text-green-500 dark:text-green-500 text-2xl font-semibold">Payment Successful 😊!</h2>
          <h2 v-else class="text-red-500 dark:text-red-500 text-2xl font-semibold">QR Code Expired</h2>
          <div v-if="qrCodeSrc && isValid" class="my-4">
            <img :src="qrCodeSrc" alt="QR Code" class="w-full h-auto">
            <p class="text-gray-600 mt-2">This QR code is valid for the next 30 minutes , and will be stored on the QRCodes page.</p>
          </div>
          <p v-if="!isValid" class="text-red-500 dark:text-red-500">Your QR code has expired. Please initiate a new transaction.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import Navbar from './Navbar.vue';
import { isDarkMode } from '@/state.js';


const qrCodeSrc = ref(null);
const isValid = ref(true);
let validityCheckInterval;

const fetchQRCode = async () => {
  const route = useRoute();
  const paymentId = route.query.paymentId;
  try {
    const response = await axios.post('http://localhost:5000/generate-qr', { payment_id: paymentId });
    qrCodeSrc.value = 'data:image/png;base64,' + response.data.qr_image;
  } catch (error) {
    console.error('Error fetching QR code:', error);
  }
};


const checkValidity = async () => {
  const route = useRoute();
  const paymentId = route.query.payment_id;
  try {
    const response = await axios.get(`http://localhost:5000/check-qr-validity/${paymentId}`);
    isValid.value = response.data.is_valid;
    if (!isValid.value) {
      clearInterval(validityCheckInterval);
    }
  } catch (error) {
    console.error('Error checking QR code validity:', error);
  }
};

const startValidityCheck = () => {
  validityCheckInterval = setInterval(checkValidity, 5 * 60 * 1000);
};

onMounted(() => {
  fetchQRCode();
  startValidityCheck();
});

onBeforeUnmount(() => {
  clearInterval(validityCheckInterval);
});
</script>

<style scoped>
/* Your styles here */
</style>
