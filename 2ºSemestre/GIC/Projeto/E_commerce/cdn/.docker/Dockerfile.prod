FROM nginx:1.26.3-alpine

COPY ./API/wwwroot/images /default-images
COPY ./cdn/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80