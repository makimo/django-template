<template>
    <div class="cc-column">
        <div class="cc-description">
            <slot></slot>
        </div>
        <GdprToggle :name="permission" />
    </div>
</template>

<script setup>
import GdprToggle from './gdpr_toggle.vue';

defineProps({
    permission: String,
});
</script>
