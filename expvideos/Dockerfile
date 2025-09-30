# syntax=docker/dockerfile:1
FROM node:22-alpine

WORKDIR /app

# COPY package*.json ./
COPY . .
RUN npm install --production
RUN sudo apt install postgresql-client 

COPY . .

CMD ["node", "app.js"]

EXPOSE 3000