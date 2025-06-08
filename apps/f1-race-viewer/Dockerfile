FROM nginx:1.28.0-alpine3.21-perl

COPY ./dist/apps/f1-race-viewer /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]
