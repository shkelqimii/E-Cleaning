<template>
    <div :class="isDarkMode ? 'dark' : ''" class="transition-all duration-500 min-h-screen font-sans">

        <!-- Navbar -->
        <Navbar />

        <!-- Main Content -->
        <div v-if="product" class="bg-white dark:bg-gray-900 py-16 ">
            <div class="container mx-auto px-4">

                <!-- Flex layout for images and product details -->
                <div class="flex flex-wrap -mx-4 mb-10">

                    <!-- Images Section -->
                    <div class="w-full lg:w-1/2 px-4 lg:mb-0">
                        <!-- Main Image -->
                        <div @dblclick="toggleZoom" class="image-container border rounded-md overflow-hidden mb-8 cursor-pointer relative hover:shadow-lg transition-shadow">
                            <img :src="'http://localhost:5000/uploads/' + selectedImage" :alt="product.name" class="w-full h-auto transform transition-transform hover:scale-105" :class="isZoomed ? 'scale-7' : ''">
                        </div>


                        <!-- Thumbnails -->
                        <div class="flex space-x-4">
                            <div v-for="image in product.images" :key="image" class="w-1/4 cursor-pointer bg-white hover:border-blue-500 rounded-lg hover:ring-2 hover:ring-blue-500 transition-all">
                                <img @click="selectImage(image)" :src="'http://localhost:5000/uploads/' + image" :alt="product.name" class="w-full h-32 object-contain rounded-lg hover:opacity-80 transition-opacity">
                            </div>
                        </div>
                    </div>

                    <!-- Product Details Section -->
                    <div class="w-full lg:w-1/2 px-4 mt-12 lg:mt-0">
                        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
                            <h1 class="text-4xl font-bold mb-4">{{ product.name }}</h1>
                            <div v-if="product.original_price && product.original_price > product.price" class="mb-6">
                                <p class="text-gray-500 dark:text-gray-400 line-through">
                                    Original Price: €{{ product.original_price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}
                                </p>
                                <p class="text-red-600 font-semibold">
                                    Save {{ calculateDiscount(product) }}%
                                </p>
                                <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                                    Sale Price: €{{ product.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}🎉
                                </p>
                            </div>
                            <div v-else class="text-2xl font-semibold text-gray-900 dark:text-white">
                                Price: €{{ product.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}
                            </div>


                            <div class="text-x1 mb-6 font-bold">Quantity:{{ product.quantity }}</div>
                            <div class="product-description-container mb-8">
                                <div class="product-description">
                                    {{ product.description }}
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="space-y-4">
                                <button @click="addToCart" class="mr-14 py-3 px-6 text-white bg-gradient-to-r from-indigo-500 to-sky-500  shadow-md  rounded-full ">Add to Cart</button>
                                <button v-if="isAdminOrWorker" @click="editProduct" class="mr-2 py-4 px-5 text-white bg-gradient-to-r from-green-500 to-green-700 shadow-md  rounded-full "><font-awesome-icon icon="pen-to-square" /></button>
                                <button v-if="isAdminOrWorker" @click="deleteProduct" class="py-4 px-5 text-white bg-gradient-to-r from-red-600 to-pink-500 hover:from-pink-600 shadow-md  rounded-full "><font-awesome-icon icon="trash-can-arrow-up" /></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { isDarkMode } from '@/state.js';


const router = useRouter();
const route = useRoute();
const product = ref(null);
const user = ref(null);  // Adding user ref


// Selected image ref
const selectedImage = ref('');

// Zoom state
const isZoomed = ref(false);

onMounted(async () => {
    try {
        const userResponse = await axios.get('http://localhost:5000/user_details');
        if (userResponse.data) {
            user.value = userResponse.data;  // Set the user data
        }

        const productResponse = await axios.get(`http://localhost:5000/product/${route.params.id}`);
        product.value = productResponse.data;

        if (product.value.images && product.value.images.length > 0) {
            selectedImage.value = product.value.images[0];
        } else {
            selectedImage.value = ''; // or a default image path
        }

    } catch (error) {
        console.error('Failed to fetch user or product details:', error);
    }
});

// Computed property for admin or worker check
const isAdminOrWorker = computed(() => {
  return user.value && (user.value.role === 'admin' || user.value.role === 'worker');
});

// Methods
const selectImage = (image) => {
    selectedImage.value = image;
    isZoomed.value = false; // Reset zoom when changing image
};

const toggleZoom = () => {
    isZoomed.value = !isZoomed.value;
};

const deleteProduct = async () => {
    try {
        await axios.delete(`http://localhost:5000/product/${route.params.id}`);

        router.push({ name: 'ProductsList' }); // Redirect to product list after successful deletion
    } catch (error) {
        console.error(`Failed to delete product with ID: ${route.params.id}`, error);
    }
};

const editProduct = () => {
    router.push({ name: 'EditProduct', params: { id: product.value.id } });
};

const addToCart = async () => {
    try {
        await axios.post(`http://localhost:5000/cart`, {
            product_id: product.value.id,
            quantity: 1  // Assuming adding 1 product at a time; modify as needed
        });
        alert('Product added to cart successfully!'); // Notify the user
         router.push({ name: 'Cart' }); // Navigate to the cart page
    } catch (error) {
        console.error('Failed to add product to cart:', error);
    }
};

const calculateDiscount = (product) => {
    if (!product.original_price) return '0';
    const discount = ((product.original_price - product.price) / product.original_price) * 100;
    return Math.round(discount); // Rounds to nearest whole number
};



</script>

<style scoped>
.container {
  max-width: 1280px;
}

.product-image {
    width: 200px;
    height: 200px;
    overflow: hidden;

}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Styles for image container */
.image-container {
    width: 100%; /* Fixed width for all images */
    height: 300px; /* Fixed height for all images */
    overflow: hidden; /* Ensures that parts of the image outside the container are not shown */
    border-radius: 15px; /* Optional: for rounded corners */
    display: flex; /* To center the image inside the container */
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically */
    background-color: white; /* Set background color to white */

}

/* Styles for images */
.image-container img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain; /* Ensures the entire image is visible */
}




/* Container for product description */
/* Container for product description */
.product-description-container {
    max-height: 200px; /* Adjust as needed */
    overflow-y: auto;
    -webkit-overflow-scrolling: touch; /* For smooth scrolling on iOS */
    padding: 8px;
    text-align: justify;
}

/* Style for product description text */
.product-description {
    padding: 8px; /* Add padding for better readability */
    text-align: justify; /* Optional: for better text alignment */
}



/* You can add additional dark mode styles here if needed */
</style>
