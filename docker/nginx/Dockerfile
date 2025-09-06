FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/

# Create directories for static files
RUN mkdir -p /static /media

# Set proper permissions
RUN chown -R nginx:nginx /static /media

EXPOSE 80 443