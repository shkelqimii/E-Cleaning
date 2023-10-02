import './assets/tailwind.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios';


// Font Awesome imports
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faCheck, faHouse , faUserPlus , faRightFromBracket , faTrashCanArrowUp, faPenToSquare , faArrowRight, faArrowLeft , faUsers, faUserSecret, faGear} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const app = createApp(App)

axios.defaults.withCredentials = true;

// Add Font Awesome icons to the library
library.add(faUser, faCheck, faHouse ,faUserPlus, faRightFromBracket, faTrashCanArrowUp, faPenToSquare , faArrowRight, faArrowLeft, faUsers, faUserSecret, faGear);

// Register the Font Awesome component globally
app.component('font-awesome-icon', FontAwesomeIcon);

app.use(createPinia())
app.use(router)

app.mount('#app')