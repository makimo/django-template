# Installation

```
pip install cookiecutter
cookiecutter git@github.com:makimo/django-template.git
```

# Development

```
git clone git@github.com:makimo/django-template.git      # to one directory

cookiecutter [path to local directory]/django-template/     # to another

[ make changes + test ]
[ apply changes in template repository ]
[ commit changes ]

```

All of the project files are NOT in the base directory. They are in the
`{{ cookiecutter.project_slug }}` directory. Top-level directory is used
for cookiecutter files and repository settings.

## Quickstart Makefiles

Put your own quickstart initialization into the
`{{ cookiecutter.project_slug }}/quickstart` directory. See `dragonee.mk` for reference.

Some rules if you are going to write your own Makefile.

- The targets should follow closely README chapters with your toolkit of choice.
- Do not automate anything that is not in README.
- Do not modify global Makefile unless acknowledged by majority of the team.

# Asset directory structure

```
assets/
   ├── app.js
   ├── vendor.js
   ├── apps.scss
   ├── components/
   │       ├── hello_world.vue
   │       ├── hello_world_mount.js
   │       └── ... [.vue/.js]
   ├── images/
   │      └── ... [.png/.jpg]
   ├── scripts/
   │      ├── vendor/
   │      │     └── ... [.js]
   │      └── ... [.js]
   ├── styles/
   │     └── ... [.css/.scss]
   └── vendor
         └── ...
```

### app.js

Application code-base entry point. Normally, this file is used to
load application dependencies such as scripts in `scripts/` and
`app.scss`.

### vendor.js

Loads vendor dependencies (e.g. front-end themes such as Material Admin).

### apps.scss

Main entry-point for application-wide styles. Loads files in `styles/`.

### components/

Vue's single-page applications and their mount scripts.

### scripts/

Vanilla JavaScript front-end scripts. Those usually rely on jQuery + AJAX.

### scripts/vendor/

Subset of JavaScript scripts related to 3rd party library usage, such
as initialisation of plugins.

### styles/

Application-wide styles divided into logical components (such as related
to header, sidebar, search-bar and so on).

### vendor/

Vendor dependencies (see `vendor.js`).

# Webpack generated files

1. `runtime` - Shared runtime Webpack code. Extracted for performance from
`vendor` and `app`.

2. `app` - Application-specific code-base, i.e. stuff that programmer writes.

3. `vendor` - Scripts compiled from vendor dependencies (such as front-end
themes).

4. `common` - Shared dependencies compiled from `vendor` and `app`, e.g.
jQuery. This file will not be generated if no shared dependencies are
detected by Webpack.

5. `shared` - Shared utilities and helpers.

# Issues

Report all issues under this repository Issues page.

