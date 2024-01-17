<template>
    <div :class="{ 'dark': isDarkMode }" class="transition-all duration-500 min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      <Navbar />
  
      <!-- Sticky Search and Filter Bar -->
      <div class="sticky-container  dark:bg-gray-800 shadow-lg">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center ">
          <!-- Attractive Modern Search Bar -->
          <div class="relative flex-grow mr-4  ">
            <input v-model="searchQuery" type="text" placeholder="Explore our products..." class="w-full pl-12 pr-4 py-3 rounded-full border-2 border-transparent border-indigo-600 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-300 focus:ring-2 focus:ring-indigo-600 focus:outline-none transition duration-100">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center justify-center"><font-awesome-icon icon="magnifying-glass" />

                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10a4 4 0 114 4H8z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6"/>
            </div>
          </div>
  
          <!-- Filter Dropdown -->
          <div class="relative">
            <select v-model="selectedFilter" class="appearance-none w-full bg-transparent py-3 pl-3 rounded-full border-2 border-gray-300 dark:border-gray-700 focus:outline-none transition duration-300 hover:border-indigo-600">
              <option value="default" >Filter</option>
              <option value="lowToHigh">Low to High</option>
              <option value="highToLow">High to Low</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
              <svg class="fill-current h-6 w-6 transform rotate-90" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M5.293 9.293L10 14.586l4.707-4.293a.999.999 0 111.414 1.414l-5 5a.999.999 0 01-1.414 0l-5-5a.997.997 0 010-1.414.999.999 0 011.414 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
  

      
        <div id="my-scrollbar" class="container mx-auto px-3 py-3">
  

        <!-- Grid for Products -->
        <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3 mb-8">
          <div v-for="product in filteredProducts" :key="product.id" class="relative bg-white dark:bg-gray-600 rounded-lg overflow-hidden shadow-md">

            <!-- Product Image with Discount Badge -->
            <div class="relative w-full h-48">
              <!-- Discount Badge -->
              <div v-if="product.original_price && product.original_price > product.price" 
                  class="absolute top-0 right-0 bg-red-500 text-white text-xs font-semibold px-2 py-2 rounded-full m-1">
                -{{ calculateDiscount(product) }}%
              </div>

              <!-- Product Image -->
              <img v-if="product.images && product.images.length > 0"
                  :src="'http://localhost:5000/uploads/' + product.images[0]"
                  alt="product image"
                  class="w-full h-full object-contain"
                  loading="lazy" />
                </div>

                <!-- Product Info -->
                <div class="product-info p-4">
                    <!-- Product Name -->
                    <router-link :to="{ name: 'ProductDetail', params: { id: product.id } }"
                                class="product-name text-lg block mb-1 hover:text-blue-600 dark:text-gray-300 transition-colors duration-300 ease-in-out">
                        {{ product.name }}
                    </router-link>

                    <div v-if="product.original_price && product.original_price > product.price" class="mb-1">
                      <p class="original-price line-through text-gray-500 ">€{{ product.original_price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}</p>
                      <p class="sale-price text-lg font-bold">€{{ product.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}</p>
                      <!-- <p class="discount-percentage text-red-600">-{{ calculateDiscount(product) }}%</p> -->
                    </div>
                    <!-- Current Price if no discount -->
                    <div v-else class="sale-price text-lg font-bold">€{{ product.price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') }}</div>
                  </div>
            </div>
        </div>

        <!-- Load More Button -->
        <button v-if="moreProductsAvailable" @click="loadMoreProducts" class="load-more-btn text-white bg-gradient-to-r from-indigo-500 to-sky-500 py-3 px-6 rounded-full m-auto block mb-15">
            Load More
        </button>
        <p v-else class="mb-15">End of Results</p>
      </div>
    </div>

</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { isDarkMode } from '@/state.js';
import Scrollbar from 'smooth-scrollbar';



const products = ref([]);
const searchQuery = ref('');
const selectedFilter = ref('default');
const start = ref(0);
const limit = 30; // Set the limit for the number of products to fetch each time
const moreProductsAvailable = ref(true);




onMounted(async () => {
    try {
        const response = await axios.get('http://localhost:5000/products');
        products.value = response.data;
    } catch (error) {
        console.error('Failed to fetch products:', error);
    }
});



const filteredProducts = computed(() =>{
    let filtered = products.value;

    if (searchQuery.value) {
        filtered = filtered.filter(products =>
            products.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
    }

    switch (selectedFilter.value){
        case 'lowToHigh':
            return filtered.sort((a, b) => a.price - b.price);
        case 'highToLow':
            return filtered.sort((a, b) => b.price - a.price);
        default:
            return filtered;
    }
})

onMounted(async () => {
    await loadMoreProducts(); // Load the first batch of products
});

// Method to fetch products with pagination
const fetchProducts = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/products?start=${start.value}&limit=${limit.value}`);
        if (start.value === 0) {
            products.value = response.data;
        } else {
            products.value = [...products.value, ...response.data];
        }
        start.value += limit.value; // Update start for next batch
    } catch (error) {
        console.error('Failed to fetch products:', error);
    }
};

// Method to load more products
const loadMoreProducts = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/products?start=${start.value}&limit=${limit}`);
        const newProducts = response.data;
        if (start.value === 0) {
            products.value = newProducts;
        } else {
            products.value = [...products.value, ...newProducts];
        }
        start.value += newProducts.length;

        // Check if the number of products returned is less than the limit
        if (newProducts.length < limit) {
            moreProductsAvailable.value = false;
        }
    } catch (error) {
        console.error('Failed to fetch products:', error);
    }
};


const calculateDiscount = (product) => {
        if (!product.original_price) return '0';
        const discount = ((product.original_price - product.price) / product.original_price) * 100;
        return Math.round(discount); // This will round the discount to the nearest whole number

    };


onMounted(() => {
  Scrollbar.init(document.querySelector('#my-scrollbar'), {
    damping: 0.1, // Adjust this value for the scroll speed
    // ... other options if needed ...
  });
});


</script>


<style scoped>
.content-container {
    overflow-y: auto;
    max-height: calc(100vh - 64px); /* Assuming 64px is the height of your Navbar */
}

.sticky-container {
  position: sticky;
  top: 0;
  z-index: 1000; /* High z-index to ensure it stays on top */
  background-color: inherit; /* To maintain the background, or set a specific color */
}

.product {
    max-width: 300px;
    display: flex;
    flex-direction: column;
}


.original-price {
        color: #999;
    }

    .sale-price {
        color: #333;
        font-weight: bold;
    }

    .discount-percentage {
        color: red;
        font-weight: bold;
    }

.product-image {
    background-color: rgb(220, 219, 219, 203, 203);
    height: 8rem; /* Adjust the height as needed */
}

.product-info {
    padding-top: 20px;
    flex-grow: 1; /* Ensure the content area fills available space */
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* Align items to top and bottom */
}

.product-name {
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Number of lines you want */
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 2.4em; /* Adjust based on your design (2 times line-height) */
    font-size: 1em; /* Adjust font size as needed */
    margin-bottom: 1em;
    line-height: 1.2em;
}

.product-price {
    text-align: left;
}

.flex.justify-between.items-center.mb-6.space-x-4.rounded-lg.shadow-xl.p-4.duration-300 {
    position: sticky;
    top: 0;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.mb-15 {
    margin-bottom: 5rem/* 48px */;
}

.container {
    scroll-behavior: smooth;
}

input, select {
    transition: all 0.9s ease; /* Smooth transition for all changes */
}

.product {
    transition: transform 2s ease; /* Smooth transition for product hover */
}


#my-scrollbar {
  max-height: calc(100vh - 64px); /* Adjust based on your navbar height */
  overflow: hidden;
}

/* Ensure that the sticky container sticks to the top */
.sticky-container {
  position: sticky;
  top: 0;
  z-index: 10; /* Higher z-index to stay above other content */
}

</style>