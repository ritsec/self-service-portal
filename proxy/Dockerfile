# Based on the official nginx image
FROM nginx

# Copy over nginx configuration files
COPY nginx.conf /etc/nginx/nginx.conf

# Remove default configuration files
RUN rm /etc/nginx/conf.d/default.conf

# Copy over crypto goodness
COPY cert.pem /etc/nginx/cert.pem
COPY key.pem /etc/nginx/key.pem

# Expose port 443 for running webserver
EXPOSE 80