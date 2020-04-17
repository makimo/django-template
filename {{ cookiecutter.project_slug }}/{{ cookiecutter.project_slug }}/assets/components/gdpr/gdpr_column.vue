<template>
    <div class="cc-column">
        <div class="cc-description">
            <slot></slot>
        </div>

        <gdpr-toggle :name="permission" />
    </div>
</template>

<script>
import GDPRToggle from './gdpr_toggle';

export default {
    name: 'GDPRColumn',

    props: {
        permission: String,
    },

    components: {
        'gdpr-toggle': GDPRToggle,
    },
}
</script>