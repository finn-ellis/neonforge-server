# frontend.Dockerfile

# --- STAGE 1: Build the React application ---
FROM node:22-alpine AS builder


# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the production-ready static files
RUN npm run build


# --- STAGE 2: Serve the application with NGINX ---
FROM nginx:stable-alpine

# Copy the built static files from the 'builder' stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy the custom NGINX configuration file
# This file will be created in the root of your project
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the outside world
EXPOSE 80
EXPOSE 81

# Start NGINX when the container launches
# CMD ["nginx", "-g", "daemon off;"]