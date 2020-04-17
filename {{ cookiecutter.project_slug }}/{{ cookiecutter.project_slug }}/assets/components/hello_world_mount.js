import Vue from 'vue'
import VueCookies from 'vue-cookies';
import Vuex from 'vuex'
import HelloWorldComponent from './hello_world.vue'

import gdpr from './gdpr/gdpr.vue';
import { gdprConfig } from './gdpr/gdpr.js';
import './../styles/gdpr.scss';

Vue.use(Vuex);
Vue.component('gdpr', gdpr);
Vue.use(VueCookies);

const store = new Vuex.Store({
    modules: {
        // It's required to name store module as gdpr.
        gdpr: gdprConfig({
            permissions: {
                // Change default value for required property.
                personalization: {
                    required: true,
                },
                // Add new permission to store.
                example: {
                    name: 'example',
                    cookieName: 'gdpr-example',
                    required: false,
                    value: window.$cookies.get('gdpr-example'),
                }
            }
        }),
    },
});

new Vue({
    store,
    render: h => h(HelloWorldComponent)
}).$mount('#app')
