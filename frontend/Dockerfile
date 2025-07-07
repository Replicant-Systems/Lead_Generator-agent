FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install lucide-react

COPY . .

EXPOSE 3000
CMD ["npm", "start"]