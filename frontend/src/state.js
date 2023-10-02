import { ref } from 'vue';

const storedDarkMode = localStorage.getItem('dark-mode');
export const isDarkMode = ref(storedDarkMode ? JSON.parse(storedDarkMode) : false);

