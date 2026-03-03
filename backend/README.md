
# SmartEat AI Backend


Este backend proporciona la lógica central, autenticación, gestión de usuarios y servicios de recomendación nutricional para la plataforma SmartEat AI. Está construido con FastAPI y PostgreSQL, integrando tecnologías de IA y ML para ofrecer recomendaciones inteligentes y seguras.

## Visión y Alcance

El backend de SmartEat AI está diseñado para ser modular, seguro y escalable. Su propósito es centralizar la lógica de negocio, autenticación y servicios de recomendación, permitiendo la integración con el frontend y otros servicios externos.

## Estructura

```
backend/
├── alembic/                 # Migraciones de base de datos
│   └── versions/            # Archivos de migraciones
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/          # Endpoints
│   ├── core/                # Utilidades principales
│   │   ├── __init__.py
│   │   ├── config_ollama.py
│   │   ├── database.py
│   │   ├── ml_model.py
│   │   ├── recommender.py
│   │   ├── security.py
│   │   └── validation.py
│   ├── crud/
│   │   ├── category.py
│   │   ├── daily_menu.py
│   │   ├── ...
│   ├── data/
│   │   ├── recipes.json
│   │   └── chroma_db_recipes/ # base de datos vectorial
│   ├── files/                 # modelo de recomendacion knn
│   │   ├── df_recetas.joblib
│   │   ├── knn.joblib
│   │   └── scaler.joblib
│   ├── models/
│   │   ├── user.py
│   │   ├── recipe.py
│   │   └── ...
│   ├── schemas/
│   │   ├── user.py
│   │   ├── recipe.py
│   │   └── ...
│   ├── seeders/          
│   │   ├── ...
│   │   ├── run_seed.py      # Script para poblar la base de datos
│   │   └── ...
│   ├── services/
│   │   ├── ...
│   │   ├── agent/           # Lógica del agente nutricional
│   │   └── ...
│   ├── utils/
├── alembic.ini
└── README.md
```
## Características

- **Arquitectura limpia**: Separación clara de modelos, esquemas, servicios y rutas para facilitar el mantenimiento y escalabilidad.
- **Autenticación JWT**: Seguridad robusta mediante PyJWT y autenticación basada en tokens.
- **Hash de contraseñas**: Bcrypt para almacenamiento seguro de credenciales.
- **Migraciones de base de datos**: Alembic para control de versiones y cambios en el esquema.
- **Tipado seguro**: Validación estricta de peticiones y respuestas con Pydantic.
- **Rutas protegidas**: Acceso seguro mediante autenticación tipo Bearer token.
- **Servicios de IA y ML**: Integración de modelos de recomendación y procesamiento de datos nutricionales.

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
   alembic upgrade head
   ```

4. **Levantar el servidor**
   ```bash
   uvicorn app.main:app --reload
   ```

## Comprobar funcionamiento correcto de la api

- `GET /` - Información de la API
- `GET /health` - Comprobación de salud

## Migraciones de base de datos
### Ejecución local y dentro del contenedor Docker

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir una migración
alembic downgrade -1

# Ver historial de migraciones
alembic history```

**IMPORTANTE:**

Cada vez que realices un cambio en los modelos de la base de datos (por ejemplo, agregar o modificar campos/tablas), debes ejecutar:

```bash
alembic revision --autogenerate -m "describe tu cambio"
alembic upgrade head
```

Esto mantendrá la base de datos sincronizada con tus modelos.

## Poblar la base de datos (Seeder)

### Ejecución local

```bash
python app/seeders/run_seed.py
```

### Ejecución dentro del contenedor Docker

```bash
PYTHONPATH=/app python -m app.seeders.run_seed
```

Este script insertará usuarios, categorías, perfiles, recetas y planes en la base de datos. Asegúrate de haber aplicado las migraciones antes de ejecutar el seeder.

## Desarrollo

Accede a la documentación interactiva de la API en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Stack tecnológico

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: Toolkit y ORM para SQL
- **Alembic**: Migraciones de base de datos
- **PyJWT**: Autenticación JWT
- **Bcrypt**: Hash de contraseñas
- **PostgreSQL**: Base de datos relacional
- **scikit-learn, joblib**: Modelos de recomendación y procesamiento de datos
- **LangChain, LangGraph**: Agentes inteligentes y flujos conversacionales
