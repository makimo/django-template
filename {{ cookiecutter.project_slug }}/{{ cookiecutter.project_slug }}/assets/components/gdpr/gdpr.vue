<template>
    <div>
        <div v-if="shouldOpenBasicModal" class="consent-cookie">
            <gdpr-basic />
        </div>
        <div v-else-if="extendOpen" class="consent-cookie">
            <gdpr-extend />
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

import GDPRBasic from './gdpr_basic';
import GDPRExtend from './gdpr_extend';

export default {
    name: 'gdpr',

    components: {
        'gdpr-basic': GDPRBasic,
        'gdpr-extend': GDPRExtend,
    },

    computed: {
        ...mapGetters([
            'shouldOpenBasicModal',
        ]),

        ...mapState({
            extendOpen: state => state.gdpr.extendOpen,
        }),
    },
}
</script>