FROM node:18-alpine

WORKDIR /app

COPY upload-server.js .
COPY public ./public

RUN npm install express multer cors

EXPOSE 3005

CMD ["node", "upload-server.js"]
