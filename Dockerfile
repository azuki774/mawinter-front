FROM nginx:1.25
COPY docker-entrypoint.d/*.sh /docker-entrypoint.d/
COPY html /usr/share/nginx/html
