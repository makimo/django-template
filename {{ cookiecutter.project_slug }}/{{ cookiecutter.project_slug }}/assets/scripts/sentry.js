import Vue from 'vue';
import * as Sentry from '@sentry/browser';
import { Vue as VueIntegration } from '@sentry/integrations';

Sentry.init({
    dsn: "<DSN>",
    integrations: [new VueIntegration({Vue, attachProps: true, logErrors: true})],
});
