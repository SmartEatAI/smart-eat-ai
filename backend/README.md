
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

## Stack tecnológico

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: Toolkit y ORM para SQL
- **Alembic**: Migraciones de base de datos
- **PyJWT**: Autenticación JWT
- **Bcrypt**: Hash de contraseñas
- **PostgreSQL**: Base de datos relacional
- **scikit-learn, joblib**: Modelos de recomendación y procesamiento de datos
- **LangChain, LangGraph**: Agentes inteligentes y flujos conversacionales
- **Ollama**: Motor LLM local para generación y embeddings

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

## Configuración e integración de Ollama

SmartEat AI utiliza Ollama como motor LLM para generación de lenguaje y embeddings, integrándose con LangChain y ChromaDB para RAG y recomendaciones personalizadas.

### Configuración en Docker

El servicio Ollama está definido en `docker-compose.yml`:

```yaml
   ollama:
      image: ollama/ollama:latest
      container_name: smarteatai_ollama
      ports:
         - "11434:11434"
      volumes:
         - ollama_data:/root/.ollama
      environment:
         - OLLAMA_CONTEXT_LENGTH=32768  # Contexto ampliado
         - OLLAMA_NUM_PARALLEL=1
         - OLLAMA_MAX_LOADED_MODELS=1
      deploy:
         resources:
            reservations:
               devices:
                  - driver: nvidia
                     count: all
                     capabilities: [ gpu ]
      entrypoint: /bin/bash
      command: -c "ollama serve"
```

Esto permite aprovechar la GPU (si está disponible) y persistir los modelos y embeddings en el volumen `ollama_data`.


### Nota sobre la base de datos vectorial (ChromaDB)

> Actualmente, la integración de la base de datos vectorial (`chroma_db_recipes`) no está activa en la lógica de recomendación. Se ha intentado implementar, pero debido a limitaciones técnicas (principalmente, la incapacidad de filtrar correctamente las recetas devueltas según las restricciones y preferencias del usuario), se ha sustituido por queries directas a la base de datos real de Postgres. La documentación y la base de datos vectorial generada (ChromaDB) se han subido igualmente al proyecto para referencia y futuras mejoras.
> Si se quiere usar, descargar el modelo de embeddings `ollama pull nomic-embed-text`.
---

### Configuración en el backend

En `backend/app/core/config_ollama.py` se inicializa el modelo y embeddings:

```python
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from app.config import settings

# Configuración para 8GB VRAM con Llama 3.1
OLLAMA_CONFIG = {
      "model": settings.OLLAMA_MODEL,
      "base_url": settings.OLLAMA_BASE_URL,
      "temperature": 0,
      "num_ctx": 16384,
      "num_predict": 4096,
}
llm = ChatOllama(**OLLAMA_CONFIG)
embeddings = OllamaEmbeddings(
      model=settings.CHROMA_EMBEDDING_MODEL, 
      base_url=settings.OLLAMA_BASE_URL
)
vector_db = Chroma(
      persist_directory=settings.CHROMA_DB, 
      embedding_function=embeddings
)
```

### Variables de entorno necesarias

Asegúrate de definir en tu `.env`:

```
OLLAMA_MODEL=llama3:latest
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_EMBEDDING_MODEL=llama3:latest
CHROMA_DB=/app/data/chroma_db_recipes
```

### Puesta en marcha de Ollama (dentro de Docker)

1. **Descarga el modelo necesario** (por ejemplo, llama3.1):
    ```bash
    ollama pull llama3.1
    ```
    Puedes cambiar el modelo en la variable `OLLAMA_MODEL`.

3. **Verifica que se ha descargado bien el modelo**:
    ```bash
    ollama list
    ```
    Deberías ver los modelos disponibles.

2. **Levanta el stack completo** (incluyendo Ollama):
    ```bash
    docker-compose up -d
    ```

4. **El backend usará Ollama automáticamente** para generación y embeddings.

### Notas
- Si tienes GPU NVIDIA, Docker usará aceleración automáticamente.
- Puedes ajustar el modelo y parámetros en el archivo `.env` y en `config_ollama.py`.
- Para más detalles, revisa la documentación oficial de [Ollama](https://ollama.com/) y [LangChain Ollama](https://js.langchain.com/docs/integrations/llms/ollama/).

## Documentación oficial

- [Ollama](https://ollama.com/)
- [Docker](https://docs.docker.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [FastApi](https://fastapi.tiangolo.com/)
- [LangChain](https://docs.langchain.com/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Scikit-Learn](https://scikit-learn.org/stable/)
