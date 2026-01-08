#!/bin/sh

set -e

# Use npm ci if lock file exists, otherwise create it with npm install
if [ -f package-lock.json ]; then
    npm ci
else
    npm install
fi

npm run dev
