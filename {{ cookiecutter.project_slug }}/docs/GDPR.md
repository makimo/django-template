# GDPR
This vue module is a ready solution for handling GDRP logic. This includes two types of modal
for handling GDPR data. One basic modal with simple buttons to accept all permissions
and then save it to cookies. In addition we've prepare also extended version
of basic modal to allow user to choose accepted permissions one by one.

All values of cookies by default are set to `"false"` or `"accepted"` values(To change that
you have to modify `falseValue` or `acceptValue` properties in `gdpr_settings`).

By default there are two available permissions for personalization and analytics +
an example permission.

## Quickstart

If you want to use GDPR module you have to add those three lines to your js file depending
from where you calling them. For example it might look like this:
```
import gdpr from './gdpr/gdpr.vue';
import { gdprConfig } from './gdpr/gdpr.js';
import './../styles/gdpr.scss';
```

Add vue components:
```
Vue.use(Vuex);
Vue.component('gdpr', gdpr);
Vue.use(VueCookies);
```

Then add store module:
```
const store = new Vuex.Store({
    modules: {
        // It's required to name store module as gdpr.
        gdpr: gdprConfig({
            permissions: {
                // Change defaults of permission.
                personalization: {
                    required: false
                },
                // Add new permission to store.
                example: {
                    name: 'example',
                    cookieName: 'gdpr-example',
                    required: false,
                    value: window.$cookies.get('gdpr-example'),
                }
            }
        })
    }
})
```

or if you want default options:
```
const store = new Vuex.Store({
    modules: {
        // It's required to name store module as gdpr.
        gdpr: gdprConfig()
    }
})
```

In the end attach gdpr tag to template and store to vue app:
```
<template>
    <div>
        <gdpr />
        <h1>Hello from the Vue component</h1>
    </div>
</template>
```

```
new Vue({
    store,
    render: h => h(HelloWorldComponent)
}).$mount('#app')
```

## Typical usage
### Change basic modal content
To change default content of basic model you have to modify `<section>` tag inside `gdpr_basic.vue`.

Example:

```
<section class="cc-content">
    <h2>Privacy policy</h2>
    <p>Example</p>

    <div v-if="linkExtendInBasic" class="cc-text-center">
        <button class="cc-button cc-button-borderless"
            @click="openExtendInBasic">Cookies settings</button>
    </div>

    <div class="cc-text-center">
        <button v-if="allPermissionsAreOptional" class="cc-button cc-button-primary-delay"
            @click="setAllFalse">Don't accept</button>
        <button class="cc-button cc-button-primary" @click="setAllTrue">Accept</button>
    </div>
</section>
```

### Change permission text in extended modal
To change default permission text you have to edit slot inside `<gdpr-column>` tag inside `gdpr_extend.vue`.

Example:

```
<gdpr-column permission="example">
    <h2>Example</h2>
    <p>More information about permission</p>
</gdpr-column>
```

### Usage in django template
Let's say we have a facebook sign in inside our page and we added html tag
script tag which loads necessary facebook javascript API:

```
<script>
  function statusChangeCallback(response) { ... }
  ...
</script>
```

and now we want to block this script when user decline mandatory permission.
You can do it with two ways:

1. Use `is_consent_accepted` template tag
    ```
    {% raw -%}
    {% is_consent_accepted 'example-cookie-name' as is_accepted %}

    {% if is_accepted %}
        <script>
        ...
        </script>
    {% endif %}
    {% endraw %}
    ```

2. Pass result of `is_consent_accepted` function to template context
    In view:
    ```
    from {{ cookiecutter.project_slug }}.apps.common.utils import is_consent_accepted

    def get(self, request):
        return render(request, {'is_accepted': is_consent_accepted('example-cookie-name')})
    ```

    In template:
    ```
    {% raw -%}
    {% if is_accepted %}
        <script>
        ...
        </script>
    {% endif %}
    {% endraw %}
    ```

### Usage in vue template
To check whenever permission was accepted or not you can use `isPermissionAccepted` getter.
This getter takes one parameter. Name of permission from store. So if one of your permission
is named `personalization` you can use it like this:
```
<div v-if="isPermissionAccepted('personalization')">
example content
</div>
...
import { mapGetters } from 'vuex';
...
computed: {
    ...mapGetters(['isPermissionAccepted'])
},
```

If you want to check if user has saved any permissions you can use `hasBasicCookie` getter.

Example:

```
<div v-if="hasBasicCookie">
example content
</div>
...
import { mapGetters } from 'vuex';
...
computed: {
    ...mapGetters(['hasBasicCookie'])
},
```

### Usage in JavaScript
We've provided some JavaScript functions. Basic example is to check if permission is accepted by user. You can achieve it with `isConsentAccepted` function. This method requires one argument, which is name of the cookie.

Example:

```
import { isConsentAccepted } from 'gdpr';

if (!isConsentAccepted('example-cookie-name')) {
    doSomething();
}
```

### Show extended modal after permissions are saved
To open extended modal you should use `openExtend` action.

Example:
```
<button @click="openExtend">Open extended modal</button>
...

...mapActions(['openExtend'])
```

## Configuration
### Add new permission
First add new permission to store. You can do it with two ways:

1. Add new permission to state inside store.
```
state: {
    permissions: {
        example: {
            name: 'example',
            cookieName: 'gdpr-example',
            required: false,
            value: window.$cookies.get('gdpr-example'),
        }
    }
}
```

2. Add new permission inside gdprConfig function.
```
gdprConfig({
    permissions: {
        example: {
            name: 'example',
            cookieName: 'gdpr-example',
            required: false,
            value: window.$cookies.get('gdpr-example'),
        }
    }
})
```

In both ways you have to specify those parameters.

* name(str) - Permission name. It is necessary to use same name for permission key in store and permission prop passed to `gdpr_column` or `gdpr_toggle`.
* cookieName(str) - Cookie name for permission.
* required(bool) - Defines if permission is required or not.
* value(str) - Defines permission value (by default it can be `falseValue` or `acceptValue`)

Also you have to provide new `<gdpr-column />` tag inside `gdpr_extend` like this:
```
<gdpr-column permission="example">
    <h2>Example</h2>
    <p>Example</p>
</gdpr-column>
```

### Remove default permissions.
To remove default permissions you have to change `permissions` object inside `gdprConfig` or in vuex store
and remove `<gdpr-column>` tags in `gdpr_extend.vue` for permissions you want to remove.

### JavaScript settings
Settings are available in `gdpr_settings.js` file inside `components/gdpr/`.

Available options:

* cookieName(str) - Name of main cookie used to determinate if user has accepted permissions. Default: `gdpr`,
* expired_at(int) - Cookies expire time. Default: `1000`,
* acceptValue(str) - Value when user has accepted permission. Default: `accepted`,
* falseValue(str) - Value when user didn't accept permission. Default: `false`,

### Django settings
In base.py django has `GDPR_SETTINGS` dict which allow you to specify any settings from django.
`GDPR_SETTINGS` are included in `gdpr` context processor so they are available in any template you use.

### State in vuex store
State properties:

* permissions(Object) - Dictionary with all permissions used in app. By default it contains
    two permissions personalization and analytics. Every permissions also includes some properties:
    * name(str) - Permission name. It is necessary to use same name for permission key in store and permission prop passed to `gdpr_column` or `gdpr_toggle`.
    * cookieName(str) - Cookie name for permission.
    * required(bool) - Defines if permission is required or not. When permission is required than toogle in `gdpr_extend` is disabled.
    * value(str) - Defines permission value(by default it's value from cookie which represent this permission)
* wasAccepted(str) - Defines if user accepted permissions or not, by default
    this value is initialized with `gdpr` cookie. Default: `window.$cookies.get('gdpr')`,
* extendOpen(bool) - Defines if extended modal should display or not. Default: `false`,
* gdprSettings(Object): Tracking settings from `base.py`. Default: `window.GDPR_SETTING`,
* linkExtendInBasic(bool): When it's true then link from `gdpr_basic` to `gdpr_extend` is going to be created. Default: true

## Reference

### Getters
Available getters:

* allPermissionsAreOptional - Returns true if all permissions are optional otherwise returns false.
* shouldOpenBasicModal - Returns true if basic modal should be display or false otherwise.
* permissionAttributes - Returns attributes for toggle buttons depending on current permission state.
    Parameters:
    * name - Permission name in store.

    Returns:
    * List with three html attributes: [css class, aria-pressed, disabled]

    Example:
    When we have permissions constructed like this in store:
    ```
    permissions: {
        personalization: {
            name: 'personalization',
            cookieName: `${cookieName}-personalization`,
            required: false,
            value: window.$cookies.get(`${cookieName}-personalization`),
        },
    },
    ```
    Then the `permissionAttributes` getter for personalization permission should look like this:
    ```
    permissionAttributes('personalization')
    ```

* isPermissionAccepted - Returns true if value in cookie specified by `cookieName` property inside permission object in the store.
    Parameters:
    * name - Permission name in store.

    Example:
    When we have permissions constructed like this in store:
    ```
    permissions: {
        personalization: {
            name: 'personalization',
            cookieName: `${cookieName}-personalization`,
            required: false,
            value: window.$cookies.get(`${cookieName}-personalization`),
        },
    },
    ```
    Then the `isPermissionAccepted` getter for personalization permission should look like this:
    ```
    isPermissionAccepted('personalization')
    ```

* hasBasicCookie - Returns true if cookie specified by `cookieName` setting exist i.e. permissions was declined or accepted by user.
* wasBasicCookieAccepted - Returns true if cookie specified by `cookieName` was accepted by user.

### Actions
Those actions are currently available:

* setAllTrue - Sets all available permissions to true and save them to cookies.
* setAllFalse - Sets all available permissions to false and save them to cookies.
* saveAllCookies - Saves all permissions with current state to cookies and close the modal.
* saveAllCookiesSlow - Saves all permissions with current state to cookies and wait 400ms to close the modal.
* openExtend - Opens extended modal.
* setToggle - Changes state of clicked toggle button. You have to send `$event` to this action.
* openExtendInBasic - Opens `gdpr_extend` in `gdpr_basic`.

### Vue components
Available vue components:

* `gdpr` - Main component containing `gdpr_basic` and `gdpr_extend`.
* `gdpr_basic` - This component includes basic GDPR modal for user.
* `gdpr_column` - Includes one column for `gdpr_extend` modal. Which consist of toggle button and description.
    Description uses vue's slot API to let you insert any html as description you want.
    Props:
    * permission(String) - Name of permission.

* `gdpr_extend` - This component includes extended GDPR modal for user.
* `gdpr_toggle` - Includes toggle buttons for `gdpr_extend` modal.
    Props:
    * name(str) - Name of permission.

### JavaScript functions

* gdprConfig - Allows you to change default gdpr configuration.
    Example:
    ```
    gdprConfig({
        permissions: {
            example: {
                name: 'example',
                cookieName: 'gdpr-example',
                required: false,
                value: window.$cookies.get('gdpr-example'),
            }
        }
    })
    ```

* getBasicConsent - Get value of cookie by `cookieName` setting.
* getConsent - Get value of any cookie specified by given name.
    Parameters:
    * name - Name of cookie.

    Example:
    ```
    getConsent('gdpr-analytics')
    ```

* hasConsent - Check if cookie specified by name was set.
    Parameters:
    * name - Name of cookie.

    Example:
    ```
    hasConsent('example-cookie-name')
    ```

* isConsentAccepted - Returns true if permission is accepted by user.
    Parameters:
    * name - Name of cookie.

    Example:
    ```
    isConsentAccepted('gdpr-analytics')
    ```

* setAcceptedConsent - Change value for cookie specified by name. Value is set to `acceptedValue` from settings.
    Parameters:

    * name - Name of cookie.

    Example:
    ```
    setAcceptedCookie('gdpr-analytics')
    ```

* setDeclinedConsent - Change value for cookie specified by name. Value is set to `falseValue` from settings.
    Parameters:
    * name - Name of cookie.

    Example:
    ```
    setDeclinedCookie('gdpr-analytics')
    ```

### Django functions
`common` app shares two functions:

* has_consent - Returns if consent cookie is available in `request.COOKIES`.
    Parameters:
    * request(HttpRequest) - Incoming request.
    * name(str) - Cookie name.
* set_consent - Sets cookie in response.
    Parameters:
    * response(HttpResponse) - Response object.
    * name(str) - Name of cookie.
* is_consent_accepted - Returns True if cookie specified by name was accepted.
    Parameters:
    * request(HttpRequest) - Incoming request.
    * name(str) - Name of cookie.


### Template tags
* `gdpr_settings` - template tag which let you add script tag with `GDPR_SETTINGS` involved.
    Example:
    ```
    {% raw %}{% load gdpr %}{% endraw %}
    {% raw %}{% gdpr_settings %}{% endraw %}
    ```

* `is_consent_accepted` - template tag which returns true if for accepted consent cookie.
    Parameters:
    * name - Name of cookie.

    Example:
    ```
    {% raw %}{% is_consent_accepted 'example-cookie-name' %}{% endraw %}
    ```
