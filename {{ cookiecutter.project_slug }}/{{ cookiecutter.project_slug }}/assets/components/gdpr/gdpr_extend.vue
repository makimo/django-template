<template>
    <div class="extend">
        <section class="cc-extended-content">
            <header class="cc-header">
                <h2>Ustawienia prywatności</h2>
                <p>W każdej chwili możesz zmienić ustawienia cookies korzystając z poniższego panelu.</p>
            </header>
            <div class="cc-toggles">
                <GdprColumn permission="personalization">
                    <h2>Personalizacja</h2>
                    <p>Korzystamy z przycisków udostępnionych przez serwis Facebook.</p>
                </GdprColumn>

                <GdprColumn permission="analytics">
                    <h2>Analiza</h2>
                    <p>Korzystamy z analizy Google, która pozwala na zbieranie danych
                    na temat korzystania z naszej strony przez użytkowników, które przesyłane są
                    do nas w celu zwiększenia jakości usługi.</p>
                </GdprColumn>

                <GdprColumn permission="example">
                    <h2>Example</h2>
                    <p>Example</p>
                </GdprColumn>
            </div>
            <div class="cc-footer">
                <button class="cc-button cc-button-secondary" @click="gdprStore.saveAllCookies()">Zapisz i zamknij</button>
                <div class="cc-bottom-panel">
                    <button class="cc-button cc-button-primary" @click="gdprStore.saveAllCookiesSlow()">Zaakceptuj wszystko</button>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { useGdprStore } from './gdpr.js';
import GdprColumn from './gdpr_column.vue';

const gdprStore = useGdprStore();
</script>
