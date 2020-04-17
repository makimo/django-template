import { expired_at, cookieName, falseValue, acceptValue } from './gdpr_settings';

function extend(destination, source) {
    Object.keys(source).map(property => {
        if (property === 'permissions') {
            extendPermissions(destination.permissions, source.permissions)
        } else {
            destination[property] = source[property];
        }
    });

    return destination;
}

function extendPermissions(destination, source) {
    Object.keys(source).map(name => extendPermissionProperties(name, destination, source));
}

function extendPermissionProperties(name, destination, source) {
    if (destination[name] === undefined) {
        destination[name] = {};
    }

    Object.keys(source[name]).map(property => destination[name][property] = source[name][property]);
}

const MUTATION_NAMES = {
    SET_ALL_TRUE: 'setAllTrue',
    SET_ALL_FALSE: 'SET_ALL_FALSE',
    SAVE_ALL_COOKIES: 'saveAllCookies',
    SAVE_ALL_COOKIES_SLOW: 'saveAllCookiesSlow',
    OPEN_EXTEND: 'openExtend',
    SET_TOGGLE: 'setToggle',
    OPEN_EXTEND_IN_BASIC: 'openExtendInBasic',
};

const state = {
    permissions: {
        personalization: {
            name: 'personalization',
            cookieName: `${cookieName}-personalization`,
            required: false,
            value: window.$cookies.get(`${cookieName}-personalization`),
        },

        analytics: {
            name: 'analytics',
            cookieName: `${cookieName}-analytics`,
            required: false,
            value: window.$cookies.get(`${cookieName}-personalization`),
        }
    },

    wasAccepted: window.$cookies.get(cookieName),

    extendOpen: false,

    gdprSettings: window.GDPR_SETTINGS,

    linkExtendInBasic: true,
};

const getters = {
    allPermissionsAreOptional: ({ permissions }) => Object.keys(permissions)
        .every((name, index, arr) => !permissions[name].required),

    shouldOpenBasicModal: ({ wasAccepted }) => wasAccepted !== acceptValue,

    permissionAttributes: ({ permissions }) => name => {
        const buttonCSSClasses = "cc-button cc-button-switch";

        // Return class, aria-pressed and disabled attributes for toggle button in gdpr_toggle.
        if (permissions[name].required) {
            return [`${buttonCSSClasses} active`, true, true];
        }

        if (permissions[name].value === acceptValue) {
            return [`${buttonCSSClasses} active`, true, false];
        }

        return [buttonCSSClasses, false, false];
    },

    isPermissionAccepted: ({ permissions }) => name => {
        return window.$cookies.get(permissions[name].cookieName) === acceptValue;
    },

    hasBasicCookie: ({ wasAccepted }) => wasAccepted !== null,

    wasBasicCookieAccepted: ({ wasAccepted }) => wasAccepted === acceptValue,
};

const actions = {
    setAllTrue({ commit }) {
        commit(MUTATION_NAMES.SET_ALL_TRUE);
    },

    setAllFalse({ commit }) {
        commit(MUTATION_NAMES.SET_ALL_FALSE);
    },

    saveAllCookies({ commit }) {
        commit(MUTATION_NAMES.SAVE_ALL_COOKIES);
    },

    saveAllCookiesSlow({ commit }) {
        commit(MUTATION_NAMES.SAVE_ALL_COOKIES_SLOW);
    },

    openExtend({ commit }) {
        commit(MUTATION_NAMES.OPEN_EXTEND);
    },

    setToggle({ commit }, event) {
        commit(MUTATION_NAMES.SET_TOGGLE, event.target.dataset.ccCookieToggle);
    },

    openExtendInBasic({ commit }) {
        commit(MUTATION_NAMES.OPEN_EXTEND_IN_BASIC);
    }
};

const mutations = {
    [MUTATION_NAMES.SET_ALL_TRUE]: (state) => {
        // Map through permissions dict, assign value to permission and set cookie.
        Object.keys(state.permissions).map((name, index) => {
            state.permissions[name].value = acceptValue;

            window.$cookies.set(
                state.permissions[name].cookieName,
                state.permissions[name].value,
                expired_at
            );
        });

        state.wasAccepted = acceptValue;
        window.$cookies.set(cookieName, acceptValue, expired_at);
    },

    [MUTATION_NAMES.SET_ALL_FALSE]: (state) => {
        Object.keys(state.permissions).map((name, index) =>
            state.permissions[name].value = falseValue);

        // Set here wasAccepted to `accepted` to close modal.
        // Cookie is not set so when user refresh the page modal still will be displayed.
        state.wasAccepted = acceptValue;
    },

    [MUTATION_NAMES.SAVE_ALL_COOKIES]: (state) => {
        // Map through permissions dict and set cookies.
        Object.keys(state.permissions).map((name, index) => {
            // Set value to `accepted` for required permissions.
            if (state.permissions[name].required) {
                state.permissions[name].value = acceptValue;
            }

            window.$cookies.set(
                state.permissions[name].cookieName,
                state.permissions[name].value,
                expired_at
            );
        });

        state.wasAccepted = acceptValue;
        window.$cookies.set(cookieName, acceptValue, expired_at);

        state.extendOpen = false;
    },

    [MUTATION_NAMES.SAVE_ALL_COOKIES_SLOW]: (state) => {
        // Map through permissions dict and set cookies.
        Object.keys(state.permissions).map((name, index) => {
            state.permissions[name].value = acceptValue;

            window.$cookies.set(
                state.permissions[name].cookieName,
                state.permissions[name].value,
                expired_at
            );
        });

        state.wasAccepted = acceptValue;
        window.$cookies.set(cookieName, acceptValue, expired_at);

        setTimeout(() => state.extendOpen = false, 400);
    },

    [MUTATION_NAMES.OPEN_EXTEND]: (state) => {
        state.extendOpen = true;
    },

    [MUTATION_NAMES.SET_TOGGLE]: (state, name) => {
        var permission = state.permissions[name];

        if (!permission) {
            throw 'Permission with given name not found in store.';
        }

        if (permission.value === acceptValue) {
            permission.value = falseValue;
        } else {
            permission.value = acceptValue;
        }
    },

    [MUTATION_NAMES.OPEN_EXTEND_IN_BASIC]: (state) => {
        // Close basic modal.
        state.wasAccepted = acceptValue;
        state.extendOpen = true;
    },
};


/**
 * Creates dict with Vuex store modules.
 * @param {Object} config 
 */
function gdprConfig(config = {}) {
    const store = {
        state,
        getters,
        mutations,
        actions,
    };

    // Merge both dictionaries.
    extend(store.state, config);
    return store;
}

function hasConsent(name) {
    return window.$cookies.get(name) !== null;
}

function setAcceptedConsent(name) {
    window.$cookies.set(name, acceptValue, expired_at);
}

function setDeclinedConsent(name) {
    window.$cookies.set(name, falseValue, expired_at);
}

function getBasicConsent() {
    return window.$cookies.get(cookieName);
}

function getConsent(name) {
    return window.$cookies.get(name);
}

function isConsentAccepted(name) {
    return windiw.$cookies.get(name) === acceptValue;
}

export {
    gdprConfig,
    hasConsent,
    setAcceptedConsent,
    setDeclinedConsent,
    getBasicConsent,
    getConsent,
    isConsentAccepted,
}
