<template>
    <div>
      <button @click="handleCheckout">Checkout</button>
    </div>
  </template>
  
  <script setup>
  import { loadStripe } from '@stripe/stripe-js';
  
  const handleCheckout = async () => {
    const stripe = await loadStripe('pk_test_51O5ONQLYq60Cyx2ypbhz9i3Xk572jV1PIaWmrwbx4TIKVqUovuhhVvAjksyMN7hslMFEjdHLs5as5E4sj33ND28b00Puxc7y5m');  // Replace with your Stripe publishable key
  
    // You'd typically fetch this from your backend.
    const session = await fetch('/create-payment-intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ amount: 2000 })  // For example, $20. Adjust as needed.
    }).then(res => res.json());
  
    if (session.clientSecret) {
      const { error } = await stripe.redirectToCheckout({
        lineItems: [{price: 'price_YOUR_PRICE_ID', quantity: 1}],  // Replace 'price_YOUR_PRICE_ID' with your Stripe price ID.
        mode: 'payment',
        successUrl: 'YOUR_SUCCESS_URL',  // Replace with your success URL
        cancelUrl: 'YOUR_CANCEL_URL',    // Replace with your cancellation URL
      });
  
      if (error) {
        console.error(error);
      }
    } else {
      console.error('Unable to fetch client secret');
    }
  };
  </script>
  