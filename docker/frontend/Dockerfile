FROM node:20-slim

WORKDIR /app

# Copiar y instalar todas las dependencias (incluidas las de desarrollo)
COPY frontend/package*.json ./
RUN npm install

# Copiar el resto del código fuente
COPY frontend .

# Construir la aplicación Next.js
RUN npm run build

# Exponer el puerto 3000
EXPOSE 3000

# Comando para iniciar el servidor de desarrollo
CMD ["npm", "run", "dev"]

# Comando para iniciar el servidor de producción (descomentar si se desea usar en producción)
# CMD ["npm", "start"]