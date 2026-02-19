-- Script de inicialización para PostgreSQL con pgvector
-- Se ejecuta automáticamente al crear el contenedor

-- Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar que la extensión está instalada
SELECT * FROM pg_extension WHERE extname = 'vector';
