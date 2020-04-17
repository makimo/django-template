<template>
    <div>
        <button type="button"
            @click="setToggle($event)"
            :data-cc-cookie-toggle="name"
            autocomplete="off"
            :class="permissionAttributes(name)[0]"
            :aria-pressed="permissionAttributes(name)[1]"
            :disabled="permissionAttributes(name)[2]">
            <div class="handle"></div>
        </button>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: 'GDPRToggle',

    props: {
        name: String,
    },

    computed: {
        ...mapGetters([
            'permissionAttributes',
        ]),
    },

    methods: {
        ...mapActions([
            'setToggle',
        ]),
    },
}
</script>
