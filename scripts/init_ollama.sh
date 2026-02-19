#!/bin/bash
# Script para inicializar Ollama con el modelo necesario
# Ejecutar después de levantar los contenedores

echo "🚀 Inicializando Ollama..."

# Verificar que el contenedor está corriendo
if ! docker ps | grep -q smarteatai_ollama; then
    echo "❌ El contenedor de Ollama no está corriendo"
    echo "Ejecuta primero: docker-compose up -d"
    exit 1
fi

echo "✅ Contenedor Ollama encontrado"

# Descargar modelo Mistral
echo "📥 Descargando modelo Mistral (puede tardar varios minutos)..."
docker exec smarteatai_ollama ollama pull mistral

if [ $? -eq 0 ]; then
    echo "✅ Modelo Mistral descargado exitosamente"
    
    # Verificar modelos instalados
    echo ""
    echo "📋 Modelos disponibles:"
    docker exec smarteatai_ollama ollama list
    
    # Prueba rápida
    echo ""
    echo "🧪 Probando modelo..."
    docker exec smarteatai_ollama ollama run mistral "Hola, responde brevemente: ¿estás funcionando?"
    
    echo ""
    echo "✨ Ollama inicializado correctamente"
    echo "Puedes usar el modelo 'mistral' en el backend"
else
    echo "❌ Error descargando modelo"
    exit 1
fi
