FROM node:23.4.0

WORKDIR /app

# Copy package.json and install dependencies
COPY frontend/package.json ./
RUN npm install

# Copy the rest of the application
COPY frontend .

# Expose the application port
EXPOSE 3000

# Command to start the development server
CMD ["npm", "run", "dev"]