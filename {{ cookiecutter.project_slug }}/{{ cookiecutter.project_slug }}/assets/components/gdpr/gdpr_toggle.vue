<template>
    <div>
        <button type="button"
            @click="handleToggle"
            :data-cc-cookie-toggle="name"
            autocomplete="off"
            :class="gdprStore.permissionAttributes(name)[0]"
            :aria-pressed="gdprStore.permissionAttributes(name)[1]"
            :disabled="gdprStore.permissionAttributes(name)[2]">
            <div class="handle"></div>
        </button>
    </div>
</template>

<script setup>
import { useGdprStore } from './gdpr.js';

const props = defineProps({
    name: String,
});

const gdprStore = useGdprStore();

const handleToggle = () => {
    gdprStore.setToggle(props.name);
};
</script>
