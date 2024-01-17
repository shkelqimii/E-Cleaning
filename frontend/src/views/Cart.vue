<template>
    <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen dark:bg-gray-900">

        <!-- Navbar -->
        <Navbar />

        <!-- Main Cart Content -->
        <div v-if="cartItems && cartItems.length > 0" class="container mx-auto max-w-screen-lg px-4 py-12">
            <h1 class="text-4xl font-bold mb-5 text-center text-gray-900 dark:text-white">My Cart</h1>

            
            <!-- <div class="flex justify-end">
                <button @click="clearCart" class="mr-4  bg-red-500 hover:bg-gray-600 text-white py-2 px-4 rounded-full transition duration-300 shadow-md mb-3 ">Clear Cart</button>
            </div> -->
            

            <!-- List of Cart Items -->
            <div v-for="item in cartItems" :key="item.product_id" class=" mb-5 p-5 bg-gray-200 dark:bg-gray-800 shadow-md rounded-xl hover:shadow-xl transition duration-300">
                <!-- Display product thumbnail -->
                <p class="mr-2 text-lg font-semibold text-gray-700 dark:text-white ">{{ item.product_name }}</p>
                <div class="flex items-center space-x-8">
                    <div class="w-1/4">
                        <img :src="'http://localhost:5000/uploads/' + item.image" alt="Product Thumbnail" class="w-full object-cover rounded-md shadow-sm">
                    </div>
                    
                    <!-- Display cart item details -->
                    <div class=" w-2/2">
                        <div class="flex justify-between items-center">
                            <p class="mr-2 text-xl text-gray-600 dark:text-gray-300">Price: €{{ item.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}</p>
                            <div class="px-3" >
                                <button @click="increaseQuantity(item)" class="mr-2 px-4 py-2 text-white bg-gradient-to-r from-green-500 to-green-700 rounded-full ">+</button>
                                <div class="mr-2 px-4 py-2 ">{{ item.quantity }}</div>
                                <button @click="decreaseQuantity(item)" class="mr-2 px-4 py-2 text-white bg-gradient-to-r from-orange-400 to-yellow-500 rounded-full">-</button>


                            </div>
                            <div class="">
                                <button @click="deleteItem(item)" class=" px-4 py-3  text-white bg-gradient-to-r from-red-500 to-pink-400 rounded-full"><font-awesome-icon icon="trash-can-arrow-up" /></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Total Price -->
            <div class="text-right mb-6">
                <strong class=" text-xl text-gray-800 dark:text-white">Total: {{ totalPrice }}€</strong>
            </div>

            <!-- Checkout & Clear Cart Buttons -->
            <div class="flex justify-end">
                <button @click="startCheckout" class="mb-12 bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-36 rounded-full">Checkout</button>
            </div>
        </div>

        <!-- Empty Cart Message -->
        <div v-else class="container mx-auto max-w-screen-lg px-4 py-12 text-center">
            <p class="text-2xl font-semibold text-gray-700 dark:text-white mb-5">Your shoping basket is empty!</p>
            <h1 class="text-9xl mb-3">😢</h1>
            <p class="text-2xl font-semibold text-gray-700 dark:text-white mb-5">Continue shoping.</p>
        </div> 
    </div>
</template>



<script setup>
    import Navbar from './Navbar.vue';
    import { ref, onMounted, computed } from 'vue';
    import axios from 'axios';
    import { isDarkMode } from '@/state.js';
    import { loadStripe } from '@stripe/stripe-js'; 

    const cartItems = ref([]);

    onMounted(async () => {
        try {
            const response = await axios.get('http://localhost:5000/cart');
            cartItems.value = response.data.cart_items;
        } catch (error) {
            console.error('Failed to fetch cart items:', error);
        }
    });

    const totalPrice = computed(() => {
    const total = cartItems.value.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    return total.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
});


    const checkProductAvailability = async (productId, desiredQuantity) => {
    try {
        const response = await axios.get(`http://localhost:5000/product/${productId}`);
        const product = response.data;
        return product.quantity >= desiredQuantity;
    } catch (error) {
        console.error('Failed to fetch product details:', error);
        return false;
    }
}


    const increaseQuantity = async (item) => {
        const isAvailable = await checkProductAvailability(item.product_id, item.quantity + 1);
        if (isAvailable) {
            item.quantity++;
            await axios.put('http://localhost:5000/cart/update', { product_id: item.product_id, quantity: item.quantity });
        } else {
            alert("You've reached the maximum available quantity for this product");
        }
    }


    const decreaseQuantity = async (item) => {
        if (item.quantity > 1) {
            item.quantity--;
            await axios.put('http://localhost:5000/cart/update', { product_id: item.product_id, quantity: item.quantity });
        } else {
            deleteItem(item);
        }
    }

    const deleteItem = async (item) => {
        const index = cartItems.value.indexOf(item);
        if (index !== -1) {
            cartItems.value.splice(index, 1);
            await axios.delete('http://localhost:5000/cart/remove', { data: { product_id: item.product_id } });
        }
    }

    const clearCart = async () => {
        cartItems.value = [];
        await axios.delete('http://localhost:5000/cart/clear');
    }

    





    const startCheckout = async () => {
    try {
        const response = await axios.post('http://localhost:5000/create-checkout-session', {
            amount: totalPrice.value
        });

        if (response.data.success) {
            const sessionId = response.data.session_id;
            const stripe = await loadStripe('pk_test_51O5ONQLYq60Cyx2ypbhz9i3Xk572jV1PIaWmrwbx4TIKVqUovuhhVvAjksyMN7hslMFEjdHLs5as5E4sj33ND28b00Puxc7y5m');
            stripe.redirectToCheckout({ sessionId: sessionId })
                .then(async result => {
                    // Check if the payment was successful. If so, clear the cart.
                    if (result.error) {
                        // Handle the error here
                        console.error('Stripe Checkout error:', result.error);
                    } else {
                        // Payment successful. Clear the cart.
                        await axios.delete('http://localhost:5000/cart/clear');
                        cartItems.value = [];
                    }
                });
        } else {
            console.error('Failed to create Stripe Checkout session');
        }
    } catch (error) {
        console.error('Error starting Stripe Checkout:', error);
    }
}

</script>

<style scoped>
    /* Modern styles for the cart page */
    p {
        color: #333;
        line-height: 1.5;
    }
    button {
        transition: all 0.3s ease;
    }
</style>