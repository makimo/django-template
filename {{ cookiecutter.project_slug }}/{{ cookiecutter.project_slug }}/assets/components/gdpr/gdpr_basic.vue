<template>
    <div class="basic">
        <section class="cc-content">
            <h2>Polityka prywatności</h2>
            <p><b>Nie zbieramy Twoich danych osobowych.</b>
                Korzystanie z tej strony jest anonimowe, jednakże potrzebujemy kilku Twoich zgód.</p>

            <div v-if="linkExtendInBasic" class="cc-text-center">
                <button class="cc-button cc-button-borderless" @click="gdprStore.openExtendInBasic()">Ustawienia plików cookie</button>
            </div>

            <div class="cc-text-center">
                <button v-if="allPermissionsAreOptional" class="cc-button cc-button-primary-delay" @click="gdprStore.setAllFalse()">Nie akceptuj</button>
                <button class="cc-button cc-button-primary" @click="gdprStore.setAllTrue()">Zaakceptuj</button>
            </div>
        </section>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useGdprStore } from './gdpr.js';

const gdprStore = useGdprStore();
const { allPermissionsAreOptional, linkExtendInBasic } = storeToRefs(gdprStore);
</script>
