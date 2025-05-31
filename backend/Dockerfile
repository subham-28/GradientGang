FROM node:18

WORKDIR /app

# Copy and install backend dependencies
COPY package*.json ./
RUN npm install

# Copy backend code
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

CMD ["node", "server.js"]
