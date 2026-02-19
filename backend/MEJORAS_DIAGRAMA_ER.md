# Mejoras al Diseño según Diagrama ER

## 📊 Cambios Implementados

### ✅ 1. Nuevo Modelo de Chat por Sesiones

**Antes:**
- Mensajes sueltos vinculados directamente al usuario
- Sin agrupación lógica de conversaciones

**Ahora (según diagrama ER):**
```
Usuario (1,1) ─── tiene ─── (1,1) Chat
Chat (1,1) ─── contiene ─── (1,N) Mensaje
Chat (1,1) ─── contiene ─── (0,N) Sugerencia
```

**Ventajas:**
- ✅ Múltiples sesiones de chat separadas por usuario
- ✅ Mejor contexto conversacional (LangChain Memory por sesión)
- ✅ Historial organizado por sesión
- ✅ Posibilidad de nombrar chats ("Plan semanal", "Ajuste proteínas", etc.)
- ✅ Navegación entre conversaciones anteriores
- ✅ Chat activo marcado con flag `activo`

---

### ✅ 2. Modelo Mensaje (antes Conversacion)

**Cambios:**
- `mensaje` → `texto` (más semántico)
- `timestamp` → `fecha_hora` (consistencia con diagrama)
- Vinculado a `chat_id` en lugar de `usuario_id` directamente
- Añadido rol `SYSTEM` para mensajes del sistema

**Estructura:**
```python
Mensaje:
  - id
  - chat_id (FK)
  - texto
  - rol (enum: user, assistant, system)
  - fecha_hora
  - contexto_plan_id (opcional)
```

---

### ✅ 3. Modelo Sugerencia (antes LogRecomendacion)

**Mejoras clave del diagrama:**
- ✅ `estado` como Enum (PENDIENTE, ACEPTADA, RECHAZADA) → más claro que boolean
- ✅ Vinculación directa a `detalle_comida_id` → sabe exactamente qué reemplazar
- ✅ `nueva_receta_id` → receta sugerida por KNN

**Metadata adicional conservada** (no en diagrama pero útil):
- `receta_original_id` → para comparación
- `distancia_knn` → métrica de similitud
- `justificacion` → explicación del LLM
- `modelo_version` → trazabilidad del modelo

**Estructura:**
```python
Sugerencia:
  - id
  - chat_id (FK)
  - detalle_comida_id (FK) ← CLAVE: sabe qué comida modificar
  - nueva_receta_id (FK)   ← La receta sugerida
  - estado (enum)
  - fecha_hora
  # Metadata adicional:
  - receta_original_id
  - distancia_knn
  - justificacion
  - modelo_version
```

---

## 🔄 Comparación: Antes vs Después

### Flujo ANTES:

```
Usuario → Conversacion (mensaje individual)
Usuario → LogRecomendacion (aceptada: True/False/None)
```

**Problemas:**
- ❌ No hay sesiones de chat separadas
- ❌ Difícil recuperar contexto conversacional
- ❌ LogRecomendacion no especifica qué detalle_comida modificar (había que inferirlo)

### Flujo AHORA (según diagrama ER):

```
Usuario → Chat (sesión) → Mensajes (conversación)
                       → Sugerencias (con estado)
```

**Ventajas:**
- ✅ Sesiones separadas con contexto claro
- ✅ Sugerencia vinculada directamente al detalle_comida
- ✅ Estado explícito (pendiente/aceptada/rechazada)

---

## 🎯 Flujo Completo de Usuario

### Escenario: Usuario quiere cambiar el almuerzo del lunes

**1. Frontend crea/reutiliza Chat:**
```http
POST /api/chat
{
  "chat_id": null,  // Nuevo chat
  "mensaje": "Quiero cambiar el almuerzo del lunes",
  "contexto_plan_id": 123
}
```

**2. Backend:**
- Si `chat_id` es null → crea nuevo Chat
- Guarda Mensaje (usuario)
- Ejecuta agente LangChain con contexto del Chat
- Agente consulta KNN → encuentra receta similar
- Crea Sugerencia con estado=PENDIENTE
- Guarda Mensaje (assistant)
- Retorna respuesta + sugerencia

**3. Frontend muestra card:**
```
╔═══════════════════════════════════════╗
║ 💡 Sugerencia                         ║
╠═══════════════════════════════════════╣
║ Original: Ensalada César (350 cal)    ║
║ Sugerida: Bowl Quinoa (380 cal)       ║
║                                       ║
║ Similitud: 95%                        ║
║ Distancia KNN: 0.12                   ║
║                                       ║
║ Justificación: Esta receta tiene      ║
║ perfil proteico similar pero mayor    ║
║ contenido de fibra...                 ║
║                                       ║
║  [✅ Aceptar]  [❌ Rechazar]          ║
╚═══════════════════════════════════════╝
```

**4. Usuario acepta:**
```http
POST /api/sugerencias/{sugerencia_id}/aceptar
```

**5. Backend:**
- Actualiza `Sugerencia.estado = ACEPTADA`
- Actualiza `DetalleComida.receta_id` con nueva receta
- Actualiza `Plan.fecha_modificacion`
- Retorna confirmación

**6. Frontend actualiza vista:**
- Muestra nuevo plan con receta reemplazada
- Marca sugerencia como aceptada en historial

---

## 💾 Migración de Datos

Las tablas antiguas (`conversaciones`, `logs_recomendaciones`) se mantienen temporalmente por compatibilidad:

```python
# DEPRECATED: Mantener compatibilidad temporal
# conversaciones = relationship("Conversacion", ...)
# logs_recomendaciones = relationship("LogRecomendacion", ...)
```

**Script de migración (futuro):**
```python
# Migrar conversaciones → chats + mensajes
# Migrar logs_recomendaciones → sugerencias
```

---

## 🚀 Próximos Pasos

### 1. Actualizar Servicios

- [x] Crear modelos: Chat, Mensaje, Sugerencia
- [x] Crear schemas: chat_v2.py
- [ ] Actualizar `ChatService` para usar Chat/Mensaje
- [ ] Actualizar `LangChainAgent` para contexto por sesión
- [ ] Implementar endpoint `POST /api/chat` (v2)
- [ ] Implementar endpoints de sugerencias

### 2. Actualizar Frontend

- [ ] Componente `ChatContainer` con lista de sesiones
- [ ] Componente `ChatWindow` para sesión activa
- [ ] Componente `SuggestionCard` mejorado con estado
- [ ] Navegación entre chats anteriores

### 3. Migración

- [ ] Crear migration Alembic con nuevas tablas
- [ ] Script de migración de datos antiguos
- [ ] Deprecar endpoints v1 gradualmente

---

## 📋 Checklist de Implementación

### Modelos (✅ Completado)
- [x] `Chat` - Sesiones de chat
- [x] `Mensaje` - Mensajes individuales
- [x] `Sugerencia` - Recomendaciones con estado
- [x] Actualizar `Usuario` relationships
- [x] Mantener modelos antiguos como DEPRECATED

### Schemas (✅ Completado)
- [x] `ChatSchema`, `ChatCreate`
- [x] `MensajeSchema`, `MensajeCreate`
- [x] `SugerenciaSchema`, `SugerenciaCreate`
- [x] Request/Response schemas actualizados

### Servicios (⏳ Pendiente)
- [ ] `ChatService` v2 con gestión de sesiones
- [ ] `SugerenciaService` para crear/actualizar sugerencias
- [ ] Actualizar `LangChainAgent` para memoria por chat_id

### API Routes (⏳ Pendiente)
- [ ] `POST /api/chats` - Crear chat
- [ ] `GET /api/chats` - Listar chats
- [ ] `GET /api/chats/{id}` - Obtener chat con historial
- [ ] `POST /api/chats/{id}/mensajes` - Enviar mensaje
- [ ] `POST /api/sugerencias/{id}/aceptar` - Aceptar sugerencia
- [ ] `POST /api/sugerencias/{id}/rechazar` - Rechazar sugerencia

### Frontend (⏳ Pendiente)
- [ ] Componente de lista de chats
- [ ] Componente de ventana de chat activo
- [ ] Card de sugerencia mejorada
- [ ] Estado de sugerencia (pendiente/aceptada/rechazada)

---

## 🎨 Diagrama de Flujo Completo

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ (1,1)
       │ tiene
       ↓
┌─────────────┐
│    Chat     │ ← Sesión de conversación
│             │   - nombre
│  id: 42     │   - fecha_creacion
│  activo: ✓  │   - activo
└──────┬──────┘
       │
       ├─(1,N)─→ ┌─────────────┐
       │          │   Mensaje   │
       │          │             │
       │          │  "Cambiar   │
       │          │   almuerzo" │
       │          └─────────────┘
       │
       └─(0,N)─→ ┌──────────────┐
                 │  Sugerencia  │
                 │              │
                 │  detalle: 15 │ ─→ DetalleComida
                 │  receta: 89  │ ─→ Receta (nueva)
                 │  estado:     │
                 │   PENDIENTE  │
                 └──────────────┘
```

---

**Conclusión:** El diseño del diagrama ER es **superior** al inicial. He implementado los nuevos modelos combinando lo mejor de ambos enfoques: la estructura limpia del diagrama + metadata útil para análisis.
