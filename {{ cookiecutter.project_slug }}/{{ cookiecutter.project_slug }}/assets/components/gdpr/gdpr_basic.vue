<template>
    <div class="basic">
        <section class="cc-content">
            <h2>Polityka prywatności</h2>
            <p><b>Nie zbieramy Twoich danych osobowych.</b>
                Korzystanie z tej strony jest anonimowe, jednakże potrzebujemy kilku Twoich zgód.</p>

            <div v-if="linkExtendInBasic" class="cc-text-center">
                <button class="cc-button cc-button-borderless" @click="openExtendInBasic">Ustawienia plików cookie</button>
            </div>

            <div class="cc-text-center">
                <button v-if="allPermissionsAreOptional" class="cc-button cc-button-primary-delay" @click="setAllFalse">Nie akceptuj</button>
                <button class="cc-button cc-button-primary" @click="setAllTrue">Zaakceptuj</button>
            </div>
        </section>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';

export default {
    name: 'GDPRBasic',

    computed: {
        ...mapGetters([
            'allPermissionsAreOptional',
        ]),

        ...mapState({
            linkExtendInBasic: state => state.gdpr.linkExtendInBasic,
        }),
    },

    methods: {
        ...mapActions([
            'setAllFalse',
            'setAllTrue',
            'openExtendInBasic',
        ]),
    },
}
</script>
