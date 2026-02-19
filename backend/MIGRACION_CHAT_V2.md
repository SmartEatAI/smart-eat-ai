# Guía de Migración: Chat V1 → Chat V2

## 📋 Resumen de Cambios

Se ha implementado la arquitectura mejorada de chat basada en el diagrama ER proporcionado. Esta versión introduce sesiones de chat, estados explícitos de sugerencias y mejor trazabilidad.

---

## 🔄 Cambios Principales

### 1. Arquitectura de Datos

**ANTES (V1):**
```
Usuario → Conversacion (mensajes individuales)
Usuario → LogRecomendacion (aceptada: bool)
```

**AHORA (V2):**
```
Usuario → Chat (sesión) → Mensajes
                        → Sugerencias (estado: enum)
```

### 2. Modelos Nuevos

#### Chat (`app/models/chat.py`)
- Representa una sesión de conversación
- Permite múltiples chats por usuario
- Campo `activo` para soft delete
- Campo `nombre` para identificar sesiones

#### Mensaje (`app/models/mensaje.py`)
- Mensajes dentro de un chat
- Enum `RolMensaje`: USER, ASSISTANT, SYSTEM
- Vinculado a `chat_id`

#### Sugerencia (`app/models/sugerencia.py`)
- Recomendaciones con estado explícito
- Enum `EstadoSugerencia`: PENDIENTE, ACEPTADA, RECHAZADA
- Vinculación directa a `detalle_comida_id`
- Metadata KNN: distancia, justificación, versión modelo

### 3. Servicios Nuevos

#### ChatServiceV2 (`app/services/chat_service_v2.py`)
- Gestión de sesiones de chat
- Procesamiento de mensajes con historial
- Integración con LangChain Agent

**Métodos principales:**
- `get_or_create_chat()` - Obtener o crear sesión
- `process_user_message()` - Procesar mensaje con agente
- `get_chat_history()` - Obtener historial completo
- `list_user_chats()` - Listar chats del usuario
- `deactivate_chat()` - Soft delete de chat

#### SugerenciaService (`app/services/sugerencia_service.py`)
- Gestión de sugerencias
- Aceptar/rechazar sugerencias
- Actualización de planes

**Métodos principales:**
- `create_sugerencia()` - Crear nueva sugerencia
- `aceptar_sugerencia()` - Aceptar y actualizar plan
- `rechazar_sugerencia()` - Rechazar con feedback
- `get_sugerencia_enriquecida()` - Obtener con datos completos

### 4. API Routes V2

**Nuevo archivo:** `app/api/routes/chat_v2.py`

#### Endpoints de Chat
```
POST   /api/chats                 - Crear nueva sesión
GET    /api/chats                 - Listar chats del usuario
GET    /api/chats/{id}            - Obtener historial de chat
DELETE /api/chats/{id}            - Desactivar chat
```

#### Endpoint de Mensajes
```
POST   /api/chat                  - Enviar mensaje al agente
```

#### Endpoints de Sugerencias
```
GET    /api/sugerencias/{id}                 - Obtener sugerencia
POST   /api/sugerencias/{id}/aceptar         - Aceptar sugerencia
POST   /api/sugerencias/{id}/rechazar        - Rechazar sugerencia
```

---

## 🚀 Migración de Frontend

### Flujo V1 (DEPRECATED)

```typescript
// Enviar mensaje
POST /api/chat
{
  "message": "Quiero cambiar el almuerzo",
  "context": {"plan_id": 123}
}

// Aceptar recomendación
POST /api/recommendations/{id}/accept
```

### Flujo V2 (NUEVO)

```typescript
// 1. Crear o reutilizar chat
POST /api/chats
{
  "nombre": "Ajuste de almuerzo"
}
// Response: { "id": 42, "nombre": "Ajuste de almuerzo", ... }

// 2. Enviar mensaje
POST /api/chat
{
  "chat_id": 42,  // null para crear nuevo
  "mensaje": "Quiero cambiar el almuerzo del lunes",
  "contexto_plan_id": 123
}
// Response:
{
  "chat_id": 42,
  "mensaje_id": 105,
  "respuesta": "He encontrado una alternativa...",
  "sugerencia": {
    "id": 201,
    "estado": "pendiente",
    "receta_nueva": { "id": 89, "name": "Bowl Quinoa", ... },
    "comparacion": { "calories_diff_pct": 8.6, ... }
  },
  "timestamp": "2026-02-19T10:30:00"
}

// 3. Aceptar sugerencia
POST /api/sugerencias/201/aceptar
// Response:
{
  "success": true,
  "message": "Receta actualizada exitosamente",
  "plan_actualizado_id": 123,
  "detalle_comida_id": 456
}

// 4. O rechazar sugerencia
POST /api/sugerencias/201/rechazar
{
  "feedback": "Prefiero recetas con menos carbohidratos"
}
```

---

## 📊 Schemas V2

### ChatMessageRequest
```typescript
{
  chat_id?: number,           // null para crear nuevo chat
  mensaje: string,            // Texto del mensaje
  contexto_plan_id?: number   // Plan en contexto
}
```

### ChatMessageResponse
```typescript
{
  chat_id: number,
  mensaje_id: number,
  respuesta: string,
  sugerencia?: SugerenciaSchema,
  timestamp: datetime
}
```

### SugerenciaSchema
```typescript
{
  id: number,
  chat_id: number,
  detalle_comida_id: number,
  nueva_receta_id: number,
  estado: "pendiente" | "aceptada" | "rechazada",
  fecha_hora: datetime,
  distancia_knn?: number,
  justificacion?: string,
  
  // Datos enriquecidos
  receta_original?: RecipeCard,
  receta_nueva?: RecipeCard,
  comparacion?: NutritionalComparison
}
```

### RecipeCard
```typescript
{
  id: number,
  name: string,
  calories: number,
  protein: number,
  carbs: number,
  fat: number,
  image_url?: string,
  recipe_url?: string
}
```

### NutritionalComparison
```typescript
{
  calories_diff_pct: number,
  protein_diff_pct: number,
  carbs_diff_pct: number,
  fat_diff_pct: number,
  
  original_calories: number,
  new_calories: number,
  original_protein: number,
  new_protein: number,
  original_carbs: number,
  new_carbs: number,
  original_fat: number,
  new_fat: number
}
```

---

## 🔧 Actualización del LangChain Agent

### Cambio Principal: Memoria por Sesión

**ANTES:**
- Memoria global compartida entre todos los usuarios
- Sin contexto histórico por sesión

**AHORA:**
- Historial del chat se recupera de BD
- Se pasa al agente en cada request
- Memoria se limpia y recarga con el historial específico

**Firma actualizada:**
```python
LangChainAgentService.run_agent(
    user_message: str,
    db_session: Session,
    chat_history: List[dict],  # NUEVO
    context: dict
)
```

**Formato de chat_history:**
```python
[
    {"role": "user", "content": "Mensaje usuario 1"},
    {"role": "assistant", "content": "Respuesta asistente 1"},
    {"role": "user", "content": "Mensaje usuario 2"},
    ...
]
```

---

## ✅ Checklist de Integración

### Backend (✅ Completado)
- [x] Modelos: Chat, Mensaje, Sugerencia
- [x] Schemas: chat_v2.py con todos los tipos
- [x] Servicios: ChatServiceV2, SugerenciaService
- [x] Routes: chat_v2.py con 8 endpoints
- [x] LangChain: Soporte para historial por sesión
- [x] Imports actualizados en __init__.py
- [x] Main.py usando chat_v2 router
- [x] Chat.py antiguo deprecado

### Frontend (⏳ Pendiente)
- [ ] Componente `ChatList` - Lista de sesiones
- [ ] Componente `ChatWindow` - Ventana de chat activo
- [ ] Componente `SuggestionCard` - Card de sugerencia mejorada
- [ ] Estado de sugerencia visual (pendiente/aceptada/rechazada)
- [ ] Integración con API V2
- [ ] Manejo de múltiples chats
- [ ] Navegación entre chats

### Base de Datos (⏳ Pendiente)
- [ ] Generar migración Alembic
- [ ] Aplicar migración en dev
- [ ] Verificar índices en chat_id, usuario_id, estado
- [ ] Script de migración de datos V1 → V2 (opcional)

---

## 🎯 Ventajas de V2

### Para Usuarios
- ✅ **Múltiples sesiones**: Diferentes conversaciones organizadas
- ✅ **Historial organizado**: Navegación clara entre chats
- ✅ **Estado claro**: Sabe qué sugerencias están pendientes/aceptadas/rechazadas
- ✅ **Contexto persistente**: El agente recuerda conversaciones anteriores en la sesión

### Para Desarrolladores
- ✅ **Mejor organización**: Código separado por responsabilidad
- ✅ **Trazabilidad**: Cada sugerencia vinculada a detalle_comida exacto
- ✅ **Escalabilidad**: Memoria por sesión evita problemas de estado compartido
- ✅ **Mantenibilidad**: Servicios separados (Chat, Sugerencia)

### Para Análisis
- ✅ **Métricas por sesión**: Duración de chats, mensajes por sesión
- ✅ **Tasa de aceptación**: Por sugerencia, no global
- ✅ **Feedback estructurado**: Razones de rechazo almacenadas
- ✅ **Versioning**: Modelo KNN usado en cada sugerencia

---

## 📝 Próximos Pasos

### 1. Base de Datos
```bash
# Generar migración
cd backend
alembic revision --autogenerate -m "Add Chat, Mensaje, Sugerencia models"

# Aplicar migración
alembic upgrade head
```

### 2. Frontend
```typescript
// Actualizar servicios API
// services/chatApi.ts
export const chatApi = {
  createChat: (nombre?: string) => 
    api.post('/chats', { nombre }),
  
  listChats: () => 
    api.get('/chats'),
  
  getChatHistory: (chatId: number) => 
    api.get(`/chats/${chatId}`),
  
  sendMessage: (chatId: number | null, mensaje: string, contexto_plan_id?: number) =>
    api.post('/chat', { chat_id: chatId, mensaje, contexto_plan_id }),
  
  acceptSuggestion: (sugerenciaId: number) =>
    api.post(`/sugerencias/${sugerenciaId}/aceptar`),
  
  rejectSuggestion: (sugerenciaId: number, feedback?: string) =>
    api.post(`/sugerencias/${sugerenciaId}/rechazar`, { feedback })
}
```

### 3. Testing
```bash
# Test endpoints
curl -X POST http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test Chat"}'

curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": null,
    "mensaje": "Hola, quiero cambiar una receta",
    "contexto_plan_id": 1
  }'
```

---

## 🔍 Backward Compatibility

### Archivos Deprecados (No Eliminar Aún)
- `app/schemas/chat_deprecated.py` - Schemas antiguos
- `app/api/routes/chat.py` - Endpoints V1 (comentado en main.py)
- `app/services/chat_service.py` - Servicio antiguo
- `app/models/conversacion.py` - Modelo antiguo (marcado DEPRECATED)
- `app/models/log_recomendacion.py` - Modelo antiguo (marcado DEPRECATED)

### Plan de Eliminación
1. **Fase 1** (actual): V2 en producción, V1 deprecado
2. **Fase 2** (2-4 semanas): Migrar frontend completamente a V2
3. **Fase 3** (1 mes): Verificar que V1 no tiene uso
4. **Fase 4** (después): Eliminar archivos V1 y modelos deprecados

---

## 📚 Recursos Adicionales

- [MEJORAS_DIAGRAMA_ER.md](MEJORAS_DIAGRAMA_ER.md) - Análisis completo del diseño
- [LANGCHAIN_SETUP.md](LANGCHAIN_SETUP.md) - Arquitectura LangChain
- [QUICKSTART.md](QUICKSTART.md) - Guía de inicio rápido

---

**Actualizado:** 2026-02-19  
**Versión:** V2.0.0  
**Estado:** ✅ Backend Completo, ⏳ Frontend Pendiente
