<template>
    <div>
        <div v-if="shouldOpenBasicModal" class="consent-cookie">
            <GdprBasic />
        </div>
        <div v-else-if="extendOpen" class="consent-cookie">
            <GdprExtend />
        </div>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useGdprStore } from './gdpr.js';
import GdprBasic from './gdpr_basic.vue';
import GdprExtend from './gdpr_extend.vue';

const gdprStore = useGdprStore();
const { shouldOpenBasicModal, extendOpen } = storeToRefs(gdprStore);
</script>
