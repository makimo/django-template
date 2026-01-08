import { createApp } from 'vue';
import { createPinia } from 'pinia';
import VueCookies from 'vue-cookies';

import HelloWorldComponent from './hello_world.vue';
import Gdpr from './gdpr/gdpr.vue';
import { useGdprStore } from './gdpr/gdpr.js';
import './../styles/gdpr.scss';

const app = createApp(HelloWorldComponent);
const pinia = createPinia();

app.use(pinia);
app.use(VueCookies);
app.component('gdpr', Gdpr);

// Configure and initialize the GDPR store
const gdprStore = useGdprStore();
gdprStore.configure({
    permissions: {
        personalization: { required: true },
        example: {
            name: 'example',
            cookieName: 'gdpr-example',
            required: false,
        }
    }
});
gdprStore.initializeCookies();

app.mount('#app');
