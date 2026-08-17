FROM nginx:alpine

# Copy conf
COPY gateway/nginx.conf /etc/nginx/nginx.conf

# Copy static file FE
COPY ../frontend /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]