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

## Testing the template

Use `test-env.py` to automatically test template generation and Docker setup:

```
./test-env.py "Test Project"           # Generate, test, and clean up
./test-env.py "Test" --no-remove       # Keep generated project after testing
./test-env.py "Test" -f                # Run Docker in foreground for manual testing
./test-env.py "Test" --clean           # Clean up existing test project
```

The script:
1. Checks prerequisites (Python, cookiecutter, Docker)
2. Generates a project from the template
3. Starts Docker services and waits for readiness
4. Runs validation checks (file structure, template substitution, Django check)
5. Cleans up all artifacts (containers, volumes, project directory)

# Asset directory structure

```
assets/
   ├── app.js
   ├── app.scss
   ├── components/
   │       ├── hello_world.vue
   │       ├── hello_world_mount.js
   │       └── ... [.vue/.js]
   ├── images/
   │      └── ... [.png/.jpg]
   ├── scripts/
   │      └── ... [.js]
   ├── styles/
   │     └── ... [.css/.scss]
   └── vendor/
         └── ... [.js]
```

### app.js

Application code-base entry point. Loads application dependencies such as
Bootstrap JS, scripts in `scripts/`, and `app.scss`.

### app.scss

Main entry-point for application-wide styles. Imports Bootstrap SCSS and
files in `styles/`.

### components/

Vue 3 single-file components and their mount scripts.

### scripts/

Vanilla JavaScript front-end scripts and shared utilities.

### styles/

Application-wide styles divided into logical components.

### vendor/

Vendor-specific scripts and initialization.

# RSBuild generated files

RSBuild compiles assets with content hashing for cache busting. For each
entry point, RSBuild generates:

1. `{entry}.[hash].js` - JavaScript bundle
2. `{entry}.[hash].css` - CSS bundle (if entry imports styles)
3. `{entry}-js-tags.html` - HTML script tags for Django templates
4. `{entry}-css-tags.html` - HTML link tags for Django templates

Entry points are defined in `rsbuild.config.mjs`. Default entries:
- `app` - Main application bundle
- `hello_world_mount` - Vue component example

# Issues

Report all issues under this repository Issues page.
