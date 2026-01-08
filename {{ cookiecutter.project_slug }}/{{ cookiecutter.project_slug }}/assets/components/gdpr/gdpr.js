import { defineStore } from 'pinia';
import { expired_at, cookieName, falseValue, acceptValue } from './gdpr_settings';

// Helper to get cookie value (works after vue-cookies is installed)
const getCookie = (name) => window.$cookies?.get(name) ?? null;

export const useGdprStore = defineStore('gdpr', {
    state: () => ({
        permissions: {
            personalization: {
                name: 'personalization',
                cookieName: `${cookieName}-personalization`,
                required: false,
                value: null,
            },
            analytics: {
                name: 'analytics',
                cookieName: `${cookieName}-analytics`,
                required: false,
                value: null,
            }
        },
        wasAccepted: null,
        extendOpen: false,
        gdprSettings: null,
        linkExtendInBasic: true,
    }),

    getters: {
        allPermissionsAreOptional: (state) =>
            Object.values(state.permissions).every(p => !p.required),

        shouldOpenBasicModal: (state) =>
            state.wasAccepted !== acceptValue,

        permissionAttributes: (state) => (name) => {
            const permission = state.permissions[name];
            const buttonCSSClasses = "cc-button cc-button-switch";

            if (permission?.required) {
                return [`${buttonCSSClasses} active`, true, true];
            }
            if (permission?.value === acceptValue) {
                return [`${buttonCSSClasses} active`, true, false];
            }
            return [buttonCSSClasses, false, false];
        },

        isPermissionAccepted: (state) => (name) =>
            getCookie(state.permissions[name]?.cookieName) === acceptValue,

        hasBasicCookie: (state) => state.wasAccepted !== null,

        wasBasicCookieAccepted: (state) => state.wasAccepted === acceptValue,
    },

    actions: {
        initializeCookies() {
            Object.keys(this.permissions).forEach(name => {
                this.permissions[name].value = getCookie(this.permissions[name].cookieName);
            });
            this.wasAccepted = getCookie(cookieName);
            this.gdprSettings = window.GDPR_SETTINGS;
        },

        configure(config) {
            if (config.permissions) {
                Object.entries(config.permissions).forEach(([name, props]) => {
                    if (!this.permissions[name]) {
                        this.permissions[name] = {
                            name,
                            cookieName: `${cookieName}-${name}`,
                            required: false,
                            value: null
                        };
                    }
                    Object.assign(this.permissions[name], props);
                });
            }
        },

        setAllTrue() {
            Object.keys(this.permissions).forEach(name => {
                this.permissions[name].value = acceptValue;
                window.$cookies.set(this.permissions[name].cookieName, acceptValue, expired_at);
            });
            this.wasAccepted = acceptValue;
            window.$cookies.set(cookieName, acceptValue, expired_at);
        },

        setAllFalse() {
            Object.keys(this.permissions).forEach(name => {
                this.permissions[name].value = falseValue;
            });
            this.wasAccepted = acceptValue;
        },

        saveAllCookies() {
            Object.keys(this.permissions).forEach(name => {
                if (this.permissions[name].required) {
                    this.permissions[name].value = acceptValue;
                }
                window.$cookies.set(this.permissions[name].cookieName, this.permissions[name].value, expired_at);
            });
            this.wasAccepted = acceptValue;
            window.$cookies.set(cookieName, acceptValue, expired_at);
            this.extendOpen = false;
        },

        saveAllCookiesSlow() {
            Object.keys(this.permissions).forEach(name => {
                this.permissions[name].value = acceptValue;
                window.$cookies.set(this.permissions[name].cookieName, acceptValue, expired_at);
            });
            this.wasAccepted = acceptValue;
            window.$cookies.set(cookieName, acceptValue, expired_at);
            setTimeout(() => { this.extendOpen = false; }, 400);
        },

        openExtend() {
            this.extendOpen = true;
        },

        setToggle(name) {
            const permission = this.permissions[name];
            if (!permission) {
                throw new Error('Permission with given name not found in store.');
            }
            permission.value = permission.value === acceptValue ? falseValue : acceptValue;
        },

        openExtendInBasic() {
            this.wasAccepted = acceptValue;
            this.extendOpen = true;
        }
    }
});

// Export helper functions for backward compatibility
export const hasConsent = (name) => getCookie(name) !== null;
export const setAcceptedConsent = (name) => window.$cookies?.set(name, acceptValue, expired_at);
export const setDeclinedConsent = (name) => window.$cookies?.set(name, falseValue, expired_at);
export const getBasicConsent = () => getCookie(cookieName);
export const getConsent = (name) => getCookie(name);
export const isConsentAccepted = (name) => getCookie(name) === acceptValue;
