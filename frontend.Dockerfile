# frontend.Dockerfile
# --- STAGE 1: Build the React application ---
FROM node:22-alpine AS builder

ARG APP_DIR
ARG WORK_DIR
ARG VITE_API_URL

WORKDIR ${WORK_DIR}
ENV VITE_API_URL=${VITE_API_URL}

# Copy package.json and package-lock.json for dependency installation
COPY ${APP_DIR}/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY ${APP_DIR}/. .

# Build the production-ready static files
RUN npm run build

RUN ls


# --- STAGE 2: Serve the application with NGINX ---
FROM nginx:stable-alpine

# Args must be declared after every "FROM"
ARG WORK_DIR
ARG APP_DIR

RUN apk add --no-cache gettext

# Copy the built static files from the 'builder' stage
COPY --from=builder ${WORK_DIR}/dist /usr/share/nginx/html

# Copy env template and entrypoint script
COPY ${APP_DIR}/public/env-template.js /usr/share/nginx/html/env-template.js
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Expose port 80 to the outside world
EXPOSE 80
EXPOSE 81

# Start NGINX when the container launches
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]