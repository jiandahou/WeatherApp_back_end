FROM node:16
WORKDIR /app
RUN npm install
EXPOSE 7990
CMD ["node", "app.js"]