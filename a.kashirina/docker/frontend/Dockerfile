FROM node:18-alpine

WORKDIR /app

# установка зависимостей
COPY package*.json ./
RUN npm install

# копирование исходного кода
COPY . .

# открытие портов
EXPOSE 3000 9229

# запуск разработки с отладкой
CMD ["npm", "run", "start:debug"] 