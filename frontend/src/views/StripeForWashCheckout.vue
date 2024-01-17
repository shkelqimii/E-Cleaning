<template>
    <div>
      <!-- Button to initiate checkout -->
      <button @click="initiateCheckout" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Buy Now
      </button>
    </div>
  </template>
  
  <script setup>
  import { loadStripe } from '@stripe/stripe-js';
  import axios from 'axios';
  
  const props = defineProps({
    productId: Number
  });
  
  const initiateCheckout = async () => {
    const stripe = await loadStripe('pk_test_51O5ONQLYq60Cyx2ypbhz9i3Xk572jV1PIaWmrwbx4TIKVqUovuhhVvAjksyMN7hslMFEjdHLs5as5E4sj33ND28b00Puxc7y5m'); // Replace with your Stripe public key
  
    try {
      const response = await axios.post('http://localhost:5000/create-washproduct-checkout-session', {
        productId: props.productId
      });
  
      if (response.data.sessionId) {
        const sessionId = response.data.sessionId;
        stripe.redirectToCheckout({ sessionId });
      } else {
        console.error('Failed to create Stripe Checkout session');
      }
    } catch (error) {
      console.error('Error initiating Stripe Checkout:', error);
    }
  };
  </script>
  