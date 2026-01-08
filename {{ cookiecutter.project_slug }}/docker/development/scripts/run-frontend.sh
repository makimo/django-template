#!/bin/sh

set -e

# Enable legacy OpenSSL provider for webpack 4 compatibility with Node.js 17+
export NODE_OPTIONS=--openssl-legacy-provider

# Use npm ci if lock file exists, otherwise create it with npm install
if [ -f package-lock.json ]; then
    npm ci
else
    npm install
fi

npm run dev
