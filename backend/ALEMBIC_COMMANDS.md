# Referencia de Comandos de Migración con Alembic

Este documento contiene los comandos esenciales de Alembic utilizados para migraciones de base de datos en el proyecto Smart Eat AI.

## Requisitos Previos

Todos los comandos deben ejecutarse desde el directorio raíz del proyecto y con el prefijo:
```bash
docker-compose exec backend alembic <comando>
```

## Comandos Comunes de Migración

### 1. Crear una Nueva Migración (Auto-generada)
Genera automáticamente una migración detectando cambios entre los modelos y la base de datos:
```bash
docker-compose exec backend alembic revision --autogenerate -m "Descripción de los cambios"
```

**Ejemplo:**
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add ON DELETE and ON UPDATE constraints to all foreign keys"
```

### 2. Crear una Nueva Migración (Manual)
Crea un archivo de migración vacío para operaciones SQL manuales:
```bash
docker-compose exec backend alembic revision -m "Descripción de los cambios"
```

### 3. Aplicar Migraciones
Actualizar la base de datos a la última migración:
```bash
docker-compose exec backend alembic upgrade head
```

Actualizar a una revisión específica:
```bash
docker-compose exec backend alembic upgrade <revision_id>
```

Actualizar un paso hacia adelante:
```bash
docker-compose exec backend alembic upgrade +1
```

### 4. Revertir Migraciones
Retroceder un paso:
```bash
docker-compose exec backend alembic downgrade -1
```

Retroceder a una revisión específica:
```bash
docker-compose exec backend alembic downgrade <revision_id>
```

Retroceder a la base (eliminar todas las migraciones):
```bash
docker-compose exec backend alembic downgrade base
```

### 5. Verificar Estado Actual de Migraciones
Mostrar la versión de migración actual:
```bash
docker-compose exec backend alembic current
```

Mostrar historial de migraciones:
```bash
docker-compose exec backend alembic history
```

Mostrar historial detallado de migraciones:
```bash
docker-compose exec backend alembic history --verbose
```

### 6. Mostrar Detalles de una Migración
Mostrar el SQL para una migración específica sin aplicarla:
```bash
docker-compose exec backend alembic show <revision_id>
```

## Comandos de Solución de Problemas

### Corregir Referencias Huérfanas de Migraciones
Si obtienes el error "Can't locate revision identified by 'xxx'":

1. Verificar la versión actual de alembic_version en la base de datos:
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "SELECT * FROM alembic_version;"
```

2. Limpiar la versión huérfana:
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "DELETE FROM alembic_version;"
```

3. Re-marcar a la migración actual:
```bash
docker-compose exec backend alembic stamp head
```

### Marcar la Base de Datos con una Revisión Específica
Marcar manualmente la base de datos como si estuviera en una revisión específica (sin ejecutar migraciones):
```bash
docker-compose exec backend alembic stamp <revision_id>
```

Marcar a la última:
```bash
docker-compose exec backend alembic stamp head
```

### Eliminar un Archivo de Migración
Si necesitas eliminar una migración incorrecta:

**Windows PowerShell:**
```powershell
Remove-Item "backend\alembic\versions\<revision_id>_descripcion.py"
```

**Windows CMD:**
```cmd
del backend\alembic\versions\<revision_id>_descripcion.py
```

**Linux/Mac:**
```bash
rm backend/alembic/versions/<revision_id>_descripcion.py
```

## Comandos de Inspección de Base de Datos

### Listar Todas las Tablas
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
```

### Describir la Estructura de una Tabla
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "\d <nombre_tabla>"
```

### Verificar Restricciones de Claves Foráneas
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "SELECT tc.table_name, tc.constraint_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name, rc.update_rule, rc.delete_rule FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name JOIN information_schema.referential_constraints AS rc ON rc.constraint_name = tc.constraint_name WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = '<nombre_tabla>';"
```

## Nuestro Proceso de Migración (Lo Que Hicimos)

### Problema Encontrado
- La migración generada tenía nombres de campos incorrectos para la tabla `usuario`
- La base de datos tenía una referencia de migración huérfana del desarrollo anterior

### Pasos Realizados

1. **Detectar el problema:**
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add ON DELETE and ON UPDATE constraints"
# Error: Can't locate revision identified by 'b1e4639b286a'
```

2. **Verificar migraciones disponibles:**
```bash
ls backend/alembic/versions/
# Solo encontramos: 382ed2ed6d7f_create_users_table.py
```

3. **Verificar estado de la base de datos:**
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "SELECT * FROM alembic_version;"
# Resultado: b1e4639b286a (referencia huérfana)
```

4. **Limpiar referencia huérfana:**
```bash
docker-compose exec -T db psql -U smarteatai -d smarteatai -c "DELETE FROM alembic_version;"
# Resultado: DELETE 1
```

5. **Re-marcar la base de datos:**
```bash
docker-compose exec backend alembic stamp head
# Running stamp_revision → 382ed2ed6d7f
```

6. **Generar nueva migración:**
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add ON DELETE and ON UPDATE constraints to all foreign keys"
# Generado: bf5ee2336f5d_add_on_delete_and_on_update_constraints_.py
```

7. **Editar manualmente el archivo de migración** para eliminar los cambios incorrectos en la tabla usuario

8. **Aplicar la migración:**
```bash
docker-compose exec backend alembic upgrade head
```

## Mejores Prácticas

1. **Siempre revisa las migraciones auto-generadas** antes de aplicarlas
2. **Usa mensajes descriptivos en las migraciones** para fácil identificación
3. **Prueba las migraciones en desarrollo** antes de producción
4. **Mantén las migraciones en control de versiones** (¡las migraciones son código!)
5. **Nunca edites migraciones ya aplicadas** - crea una nueva en su lugar
6. **Haz backup de la base de datos** antes de migraciones importantes
7. **Usa el comando `stamp` con cuidado** - no aplica SQL, solo marca el estado de la BD

## Variables de Entorno

La conexión a la base de datos está configurada en `backend/app/database.py`:
```
Database: smarteatai
User: smarteatai
Password: smarteatai123
Host: db (en la red Docker)
Port: 5432
```

## Archivos de Configuración de Alembic

- **alembic.ini**: Archivo de configuración principal
- **alembic/env.py**: Configuración del entorno de migración
- **alembic/versions/**: Directorio que contiene todos los archivos de migración
- **backend/app/models/**: Modelos de SQLAlchemy (fuente de verdad)

## Convención de Nombres de Migraciones

Alembic genera archivos de migración con este formato:
```
<revision_id>_<descripcion>.py
```

Ejemplo:
```
bf5ee2336f5d_add_on_delete_and_on_update_constraints_.py
```

Donde:
- `bf5ee2336f5d` = ID de revisión único
- `add_on_delete_and_on_update_constraints_` = Descripción sanitizada
