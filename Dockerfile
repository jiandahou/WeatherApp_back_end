FROM node:16
WORKDIR /app
COPY . /app
RUN npm install
EXPOSE 7990
CMD ["node", "app.js"]