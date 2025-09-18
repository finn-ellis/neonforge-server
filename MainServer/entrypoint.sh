#!/bin/sh
set -e

# Replace placeholders in env-template.js and create env-config.js
envsubst < /usr/share/nginx/html/env-template.js > /usr/share/nginx/html/env-config.js

# Replace placeholders in nginx template
envsubst '${NGINX_PORT},${API_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Execute the CMD
exec "$@"