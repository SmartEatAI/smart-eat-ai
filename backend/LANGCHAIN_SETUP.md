# Estructura Base LangChain - SmartEat AI

## 📁 Estructura Creada

### 🗄️ Nuevos Modelos de Base de Datos

- **`conversacion.py`**: Almacena historial de chat entre usuario y agente
- **`embedding_receta.py`**: Vectores de recetas para búsqueda semántica (384 dimensiones - all-MiniLM-L6-v2)
- **`log_recomendacion.py`**: Auditoría de recomendaciones con tracking de aceptación/rechazo
- **`modelo_ml_metadata.py`**: Versionado y metadata del modelo KNN

### 📊 Modelo Receta

Se añadió relación con embeddings para búsqueda semántica:
- Campos base: `nombre`, `calorias`, `proteinas`, `carbohidratos`, `grasas`
- URLs: `url_imagen`, `url_receta` (para info detallada de preparación)
- Relación: `embedding` (one-to-one con `EmbeddingReceta`)
- Nota: La información adicional de preparación se consulta vía `url_receta`

### 📋 Schemas Pydantic

**`schemas/chat.py`**:
- `ChatMessageRequest` / `ChatMessageResponse`
- `RecipeRecommendation` con comparación nutricional
- `AcceptRecommendationRequest` / `RejectRecommendationRequest`

**`schemas/plan.py`**:
- `PlanSchema`, `DailyMenuSchema`, `MealDetailSchema`
- `GeneratePlanRequest` / `GeneratePlanResponse`

### 🛠️ Servicios

**`services/knn_service.py`**:
- Singleton para gestionar modelo KNN
- `load_model()`: Carga modelo y scaler
- `find_similar_recipes()`: Búsqueda por vecinos cercanos (usando calorías, proteínas, carbohidratos, grasas)
- `get_feature_vector()`: Extracción y normalización de features nutricionales básicas

**`services/langchain_tools.py`**:
- `SearchSimilarRecipesTool`: Consulta KNN
- `GetRecipeDetailsTool`: Obtiene info completa de receta
- `GetUserPlanTool`: Recupera plan semanal activo
- `CompareNutritionalProfilesTool`: Compara dos recetas
- `UpdateMealInPlanTool`: Actualiza receta en plan

**`services/langchain_agent.py`**:
- Singleton para el agente LangChain
- Configuración de LLM (Ollama), Memory, Tools
- `create_agent()`: Crea instancia con sesión DB inyectada
- `run_agent()`: Ejecuta conversación

**`services/chat_service.py`**:
- `process_user_message()`: Procesa mensaje del usuario
- `accept_recommendation()`: Acepta y actualiza plan
- `reject_recommendation()`: Rechaza y registra feedback

### 🌐 API Routes

**`api/routes/chat.py`**:
- `POST /api/chat`: Enviar mensaje al agente
- `POST /api/recommendations/{id}/accept`: Aceptar recomendación
- `POST /api/recommendations/{id}/reject`: Rechazar recomendación
- `GET /api/chat/history`: Obtener historial

**`api/routes/plans.py`**:
- `GET /api/plans/active`: Plan activo del usuario
- `GET /api/plans/{id}`: Plan específico
- `POST /api/plans/generate`: Generar nuevo plan
- `GET /api/plans`: Listar planes históricos

### ⚙️ Configuración

**`config.py`** actualizado con:
- Variables Ollama: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TEMPERATURE`
- Paths KNN: `KNN_MODEL_PATH`, `KNN_SCALER_PATH`, `KNN_FEATURE_COLUMNS`
- Embeddings: `EMBEDDING_MODEL`, `EMBEDDING_DIMENSION`
- Agent: `AGENT_MAX_ITERATIONS`, `AGENT_VERBOSE`

**`requirements.txt`** actualizado con:
- LangChain: `langchain`, `langchain-community`
- LLM: `ollama`
- ML: `scikit-learn`, `joblib`, `pandas`, `numpy`, `sentence-transformers`
- DB: `pgvector`

### 🐳 Docker

**`docker-compose.yml`** actualizado:
- Base de datos cambiada a `pgvector/pgvector:pg15`
- Nuevo servicio `ollama` en puerto 11434
- Volumen `ollama_data` para persistir modelos
- Volumen `./models` montado en backend para KNN
- Script de init `docker/db/init.sql` para habilitar pgvector

**`docker/db/init.sql`**:
- Crea extensión `vector` automáticamente

## 🚀 Próximos Pasos

### 1. Migración de Base de Datos

```bash
# Generar nueva migración con todos los modelos
docker exec smarteatai_backend alembic revision --autogenerate -m "add_langchain_models"

# Aplicar migración
docker exec smarteatai_backend alembic upgrade head
```

### 2. Descargar Modelo Ollama

```bash
# Entrar al contenedor Ollama
docker exec -it smarteatai_ollama bash

# Descargar modelo Mistral (recomendado)
ollama pull mistral

# Alternativos: llama2, codellama, etc.
ollama pull llama2
```

### 3. Preparar Modelo KNN

Coloca tus archivos en `./models/`:
- `knn_nutricional.pkl`: Modelo KNN entrenado
- `scaler.pkl`: StandardScaler usado en entrenamiento (opcional)

### 4. Implementar Funciones Pendientes

Busca los `TODO` en el código:

- **knn_service.py**: 
  - [ ] Implementar lógica completa de `find_similar_recipes()`
  - [ ] Query a BD en `get_feature_vector()`
  - [ ] Query a `ModeloMLMetadata` en `get_model_info()`

- **langchain_tools.py**:
  - [ ] Implementar todas las tools (actualmente retornan placeholders)
  - [ ] Conectar con KNNService y modelos de BD

- **chat_service.py**:
  - [ ] Descomentar y configurar llamada a `LangChainAgentService.run_agent()`
  - [ ] Implementar parser de respuestas para detectar recomendaciones
  - [ ] Implementar actualización de plan en `accept_recommendation()`

- **plans.py routes**:
  - [ ] Implementar lógica de generación de planes
  - [ ] Cargar relaciones (eager loading) en queries

- **chat.py routes**:
  - [ ] Implementar endpoint de historial

### 5. Cargar Dataset de Recetas

El dataset debe incluir las columnas básicas:
- `nombre`: Nombre de la receta
- `calorias`: Calorías totales (kcal)
- `proteinas`: Proteínas (g)
- `carbohidratos`: Carbohidratos (g)
- `grasas`: Grasas totales (g)
- `url_imagen`: URL de imagen de la receta (opcional)
- `url_receta`: URL externa con información detallada de preparación

Ejecutar script de carga:
```bash
docker exec smarteatai_backend python scripts/load_recipes.py \
  --input /app/data/recetas_ejemplo.csv \
  --format csv
```

El script automáticamente genera embeddings semánticos para cada receta.

### 6. Testing

```bash
# Verificar health check
curl http://localhost:8000/health

# Debería retornar:
{
  "status": "healthy",
  "knn_loaded": true,
  "langchain_initialized": true
}

# Probar endpoint de chat
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'
```

## 📝 Notas Importantes

### Estado Actual
- ✅ Estructura de modelos completa
- ✅ Schemas Pydantic definidos
- ✅ Servicios con arquitectura completa
- ✅ Routes API creados
- ✅ Docker configurado con pgvector y Ollama
- ⚠️ Implementación de lógica de negocio **PENDIENTE** (marcada con TODOs)

### Arquitectura
- **Singleton pattern** para KNN y LangChain (una sola carga en memoria)
- **Dependency injection** de sesión DB en tools
- **Memory conversacional** con LangChain
- **Auditoría completa** de recomendaciones

### Consideraciones
- Los servicios se inicializan en el evento `startup` de FastAPI
- Las Tools de LangChain requieren sesión de DB inyectada por request
- El agente usa `ZERO_SHOT_REACT_DESCRIPTION` para razonamiento
- Los embeddings son persistentes en PostgreSQL con índice HNSW (crear en migración)

## 🔗 Referencias

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Ollama Models](https://ollama.ai/library)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Sentence Transformers](https://www.sbert.net/)

---

**Estado**: Estructura base completa ✅ | Implementación en progreso 🚧
