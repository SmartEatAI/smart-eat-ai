
# SmartEat AI Backend

Backend API construido con FastAPI, PostgreSQL y PyJWT.

## Estructura

```
backend/
├── alembic/                 # Migraciones de base de datos
│   ├── env.py               # Configuración de Alembic
│   ├── script.py.mako       # Plantilla para scripts de migración
│   └── versions/            # Archivos de migraciones generados
├── app/
│   ├── __init__.py          # Inicialización del paquete
│   ├── config.py            # Configuración de la app
│   ├── database.py          # Conexión a la base de datos
│   ├── main.py              # Punto de entrada de la app FastAPI
│   ├── api/                 # Rutas de la API
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencias (auth, etc.)
│   │   └── routes/          # Carpeta de rutas
│   │       ├── __init__.py
│   │       └── auth.py      # Rutas de autenticación
│   ├── core/                # Utilidades principales
│   │   ├── __init__.py
│   │   └── security.py      # Funciones de seguridad y JWT
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── user.py          # Modelo de usuario
│   ├── schemas/             # Esquemas Pydantic (validación)
│   │   ├── __init__.py
│   │   └── user.py          # Esquemas de usuario
│   └── services/            # Lógica de negocio
│       ├── __init__.py
│       └── auth.py          # Servicio de autenticación
├── alembic.ini              # Configuración principal de Alembic
└── README.md                # Documentación del backend                

## Características

- **Arquitectura limpia**: Separación de responsabilidades (modelos, esquemas, servicios, rutas)
- **Autenticación JWT**: Uso de PyJWT para autenticación basada en tokens
- **Hash de contraseñas**: Bcrypt para almacenamiento seguro de contraseñas
- **Migraciones de base de datos**: Alembic para control de versiones del esquema
- **Tipado seguro**: Esquemas Pydantic para validación de peticiones y respuestas
- **Rutas protegidas**: Autenticación tipo Bearer token

## Configuración

1. **Instalar dependencias**
   ```bash
   pip install -r ../docker/backend/requirements.txt
   ```

2. **Configurar variables de entorno**
   
   El archivo `.env.example` se encuentra en la raíz del proyecto. Cópialo como `.env` en la raíz:
   ```bash
   # Desde la raíz del proyecto
   cp .env.example .env
   # Edita .env con tus credenciales de base de datos y claves secretas
   ```

3. **Ejecutar migraciones**
   ```bash
   alembic revision --autogenerate -m "Migración inicial"
   alembic upgrade head
   ```

4. **Levantar el servidor**
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints de la API

### Autenticación
- `POST /api/auth/register` - Registrar un nuevo usuario
  - Valida la fortaleza de la contraseña (mínimo 8 caracteres, mayúscula, minúscula, número)
  - Devuelve un token JWT para login inmediato
- `POST /api/auth/login` - Iniciar sesión y obtener token JWT
- `GET /api/auth/me` - Obtener información del usuario actual (protegido)

### Salud
- `GET /` - Información de la API
- `GET /health` - Comprobación de salud

## Ejemplos de petición/respuesta

### Registro
```json
POST /api/auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}

Respuesta:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Login
```json
POST /api/auth/login
{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Respuesta: Igual que registro
```

### Obtener usuario actual (protegido)
```
GET /api/auth/me
Headers:
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Respuesta:
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Migraciones de base de datos

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir una migración
alembic downgrade -1

# Ver historial de migraciones
alembic history
```

**IMPORTANTE:**

Cada vez que realices un cambio en los modelos de la base de datos (por ejemplo, agregar o modificar campos/tablas), debes ejecutar:

```bash
alembic revision --autogenerate -m "describe tu cambio"
alembic upgrade head
```

Esto mantendrá la base de datos sincronizada con tus modelos.

## Desarrollo

Accede a la documentación de la API en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Stack tecnológico

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: Toolkit y ORM para SQL
- **Alembic**: Herramienta de migraciones de base de datos
- **PyJWT**: Implementación de JSON Web Token
- **Bcrypt**: Librería para hash de contraseñas
- **PostgreSQL**: Base de datos relacional
