import Vue from 'vue';
import * as Sentry from '@sentry/browser';
import { Vue as VueIntegration } from '@sentry/integrations';

const { SENTRY_DSN } = process.env;

Sentry.init({
    dsn: SENTRY_DSN,
    integrations: [new VueIntegration({Vue, attachProps: true, logErrors: true})],
});
