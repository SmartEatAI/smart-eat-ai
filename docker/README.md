# Docker

Este directorio contiene los Dockerfiles utilizados para levantar los contenedores del proyecto Smart-Eat-AI.

Estructura
- `backend/` - Dockerfile y `requirements.txt` para la imagen del backend (FastAPI).
- `frontend/` - Dockerfile para la imagen del frontend (Next.js).

Usos comunes

1) Levantar todo con `docker-compose` (desde la raíz del repositorio):

```bash
docker-compose build
docker-compose up -d
docker-compose logs -f backend
```

2) Construir y ejecutar la imagen del backend localmente:

```bash
docker build -f docker/backend/Dockerfile -t smart-eat-backend:local .
docker run --rm -p 8000:8000 --env-file .env smart-eat-backend:local
```

3) Construir y ejecutar la imagen del frontend localmente:

```bash
docker build -f docker/frontend/Dockerfile -t smart-eat-frontend:local .
docker run --rm -p 3000:3000 smart-eat-frontend:local
```

Notas
- El backend espera que las variables de entorno estén disponibles (usa un archivo `.env` en la raíz del repo cuando se ejecuta localmente).
- Si necesitas ejecutar migraciones de base de datos, usa los comandos de Alembic desde el directorio `backend/`.
- Revisa `docker-compose.yml` en la raíz para ver la configuración de redes, volúmenes y dependencias entre servicios.

Soporte
- Más información: consulta el README principal del proyecto en la raíz del repositorio.
