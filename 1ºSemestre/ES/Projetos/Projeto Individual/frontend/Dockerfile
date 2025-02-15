FROM node:18.17.0-alpine

WORKDIR /frontend

RUN npm install -g pnpm

COPY . .

RUN pnpm install

EXPOSE 3000

ENTRYPOINT ["pnpm", "dev"]