# 🎯 Guía de Inicio Rápido - LangChain Setup

## ✅ ¿Qué se ha creado?

Se ha implementado la **estructura base completa** para trabajar con LangChain en SmartEat AI:

### 📦 Componentes Creados

1. **4 Nuevos Modelos de BD** (conversacion, embedding_receta, log_recomendacion, modelo_ml_metadata)
2. **Modelo Receta** con relación a embeddings para búsqueda semántica
3. **8 Schemas Pydantic** para validación de requests/responses
4. **5 Servicios** (KNN, LangChain Agent, Tools, Chat Service)
5. **2 Nuevos Routers API** (chat, plans) con 9 endpoints
6. **Docker actualizado** con pgvector y Ollama
7. **Configuración completa** para LLM y ML
8. **Scripts de utilidad** para inicialización

---

## 🚀 Pasos para Ejecutar

### 1️⃣ Configurar Variables de Entorno

```bash
# Copiar template de configuración
cp .env.example .env

# Editar .env y cambiar SECRET_KEY
# Generar key segura con: openssl rand -hex 32
```

### 2️⃣ Reconstruir Contenedores

```bash
# Detener contenedores existentes
docker-compose down

# Reconstruir con nuevas dependencias
docker-compose build --no-cache

# Levantar servicios
docker-compose up -d
```

### 3️⃣ Aplicar Migraciones de BD

```bash
# Generar migración con nuevos modelos
docker exec smarteatai_backend alembic revision --autogenerate -m "add_langchain_models"

# Aplicar migración
docker exec smarteatai_backend alembic upgrade head
```

### 4️⃣ Inicializar Ollama

```powershell
# En Windows PowerShell
.\scripts\init_ollama.ps1

# En Linux/Mac (Git Bash en Windows)
bash scripts/init_ollama.sh
```

Esto descargará el modelo Mistral (~4.1GB). Espera 5-10 minutos.

### 5️⃣ Preparar Modelo KNN

```bash
# Crear directorio de modelos
mkdir models

# Colocar tus archivos:
# models/knn_nutricional.pkl
# models/scaler.pkl
```

### 6️⃣ Cargar Dataset de Recetas

```bash
# Preparar archivo CSV con columnas básicas:
# nombre, calorias, proteinas, carbohidratos, grasas, url_imagen, url_receta

# Ejecutar script de carga (genera embeddings automáticamente)
docker exec smarteatai_backend python scripts/load_recipes.py \
  --input /app/data/recetas_ejemplo.csv \
  --format csv
```

**Nota**: El dataset incluye 20 recetas de ejemplo. La información detallada de preparación
(ingredientes, pasos, etc.) se accede vía `url_receta` de cada receta.

### 7️⃣ Verificar Instalación

```bash
# Health check
curl http://localhost:8000/health

# Debería retornar:
# {
#   "status": "healthy",
#   "knn_loaded": true,
#   "langchain_initialized": true
# }
```

---

## 🧪 Probar el Sistema

### Test 1: Autenticación

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "correo": "test@example.com",
    "contrasena": "password123"
  }'

# Guardar el token retornado
TOKEN="..."
```

### Test 2: Chat Básico

```bash
# Enviar mensaje al agente
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, ¿puedes ayudarme con mi plan alimenticio?"
  }'
```

### Test 3: Consultar Plan

```bash
# Obtener plan activo
curl http://localhost:8000/api/plans/active \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📝 TODOs de Implementación

Los servicios tienen la estructura completa pero requieren implementación de lógica de negocio:

### Alta Prioridad

- [ ] **KNNService.find_similar_recipes()**: Implementar búsqueda real con modelo KNN
- [ ] **LangChain Tools**: Conectar con BD y KNN (actualmente retornan placeholders)
- [ ] **ChatService.process_user_message()**: Descomentar llamada a LangChain Agent
- [ ] **PlanService**: Crear servicio para generación de planes semanales

### Media Prioridad

- [ ] **Output Parser**: Crear parser para estructurar respuestas del LLM
- [ ] **Accept/Reject Recommendation**: Implementar actualización real de planes
- [ ] **Chat History**: Implementar endpoint de historial
- [ ] **Eager Loading**: Optimizar queries con relaciones

### Baja Prioridad

- [ ] **Tests unitarios**: Crear suite de tests
- [ ] **Logging avanzado**: Configurar logging estructurado
- [ ] **Métricas**: Implementar tracking de performance
- [ ] **Rate Limiting**: Añadir límites de requests

---

## 🏗️ Arquitectura

```
┌─────────────┐
│   Frontend  │ ──→ POST /api/chat
│  (Next.js)  │
└─────────────┘
       ↓
┌──────────────────────────────────┐
│     FastAPI Backend              │
│  ┌────────────────────────────┐  │
│  │   ChatService              │  │
│  │  - process_user_message()  │  │
│  └────────┬───────────────────┘  │
│           ↓                      │
│  ┌────────────────────────────┐  │
│  │  LangChain Agent Service   │  │
│  │  - Ollama LLM (Mistral)    │  │
│  │  - ConversationMemory      │  │
│  │  - Custom Tools            │  │
│  └────────┬───────────────────┘  │
│           ↓                      │
│  ┌────────────────────────────┐  │
│  │   LangChain Tools          │  │
│  │  - SearchSimilarRecipes    │  │
│  │  - GetRecipeDetails        │  │
│  │  - CompareNutritional      │  │
│  │  - UpdateMealInPlan        │  │
│  └────────┬───────────────────┘  │
│           ↓                      │
│  ┌────────────────────────────┐  │
│  │   KNN Service              │  │
│  │  - Loaded model (.pkl)     │  │
│  │  - find_similar_recipes()  │  │
│  └────────┬───────────────────┘  │
└───────────┼──────────────────────┘
            ↓
     ┌──────────────┐
     │  PostgreSQL  │
     │  + pgvector  │
     │              │
     │ - recetas    │
     │ - embeddings │
     │ - planes     │
     │ - logs       │
     └──────────────┘
```

---

## 📚 Archivos Importantes

### Modelos
- `app/models/conversacion.py` - Historial de chat
- `app/models/embedding_receta.py` - Vectores semánticos
- `app/models/log_recomendacion.py` - Tracking recomendaciones
- `app/models/receta.py` - Recetas extendidas

### Servicios
- `app/services/knn_service.py` - Modelo KNN singleton
- `app/services/langchain_agent.py` - Agente principal
- `app/services/langchain_tools.py` - Tools personalizadas
- `app/services/chat_service.py` - Lógica de chat

### API
- `app/api/routes/chat.py` - Endpoints de conversación
- `app/api/routes/plans.py` - Endpoints de planes

### Configuración
- `app/config.py` - Variables de entorno
- `docker-compose.yml` - Servicios Docker
- `docker/backend/requirements.txt` - Dependencias Python

### Scripts
- `scripts/load_recipes.py` - Cargar dataset
- `scripts/init_ollama.ps1` - Inicializar Ollama

### Docs
- `backend/LANGCHAIN_SETUP.md` - Documentación detallada

---

## 🔍 Debugging

### Ver logs de backend
```bash
docker logs -f smarteatai_backend
```

### Verificar Ollama
```bash
# Listar modelos
docker exec smarteatai_ollama ollama list

# Probar modelo
docker exec smarteatai_ollama ollama run mistral "test"
```

### Conectar a PostgreSQL
```bash
# Con psql
docker exec -it smarteatai_db psql -U smarteat_user -d smarteat_db

# Verificar pgvector
SELECT * FROM pg_extension WHERE extname = 'vector';

# Listar tablas
\dt
```

### Verificar embeddings
```sql
SELECT COUNT(*) FROM embeddings_recetas;
SELECT receta_id, modelo_version FROM embeddings_recetas LIMIT 5;
```

---

## ⚠️ Troubleshooting

### Error: "Modelo KNN no cargado"
- Verificar que `models/knn_nutricional.pkl` existe
- Revisar permisos del directorio
- Verificar logs de startup

### Error: "LangChain Agent no inicializado"
- Verificar que Ollama está corriendo: `docker ps | grep ollama`
- Verificar que Mistral está descargado: `docker exec smarteatai_ollama ollama list`
- Revisar logs de backend

### Error: "Could not resolve import"
- Es normal antes de reconstruir contenedores
- Ejecutar: `docker-compose build --no-cache`

### Error: "pgvector extension not found"
- Verificar imagen Docker: debe ser `pgvector/pgvector:pg15`
- Recrear contenedor: `docker-compose down -v && docker-compose up -d`

---

## 🎓 Próximos Pasos Recomendados

1. **Implementar KNN Service** - Es la funcionalidad core
2. **Implementar Tools** - Conectar con BD para queries reales
3. **Probar Agent end-to-end** - Verificar flujo completo
4. **Crear Plan Service** - Generar planes semanales
5. **Implementar Output Parser** - Estructurar respuestas del LLM
6. **Testing** - Crear tests unitarios y de integración
7. **Frontend** - Actualizar componentes de chat para nuevos endpoints

---

## 📞 Soporte

Busca en el código por `TODO` para encontrar implementaciones pendientes.

Cada servicio tiene comentarios explicativos sobre qué debe implementarse.

---

**Estado Actual**: ✅ Estructura completa | 🚧 Lógica de negocio pendiente

**Tiempo estimado para implementación completa**: 3-5 días de desarrollo

