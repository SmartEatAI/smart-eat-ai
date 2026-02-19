# Script para inicializar Ollama con el modelo necesario
# Ejecutar después de levantar los contenedores

Write-Host "🚀 Inicializando Ollama..." -ForegroundColor Cyan

# Verificar que el contenedor está corriendo
$ollamaRunning = docker ps --filter "name=smarteatai_ollama" --format "{{.Names}}"

if (-not $ollamaRunning) {
    Write-Host "❌ El contenedor de Ollama no está corriendo" -ForegroundColor Red
    Write-Host "Ejecuta primero: docker-compose up -d"
    exit 1
}

Write-Host "✅ Contenedor Ollama encontrado" -ForegroundColor Green

# Descargar modelo Mistral
Write-Host "📥 Descargando modelo Mistral (puede tardar varios minutos)..." -ForegroundColor Yellow
docker exec smarteatai_ollama ollama pull mistral

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Modelo Mistral descargado exitosamente" -ForegroundColor Green
    
    # Verificar modelos instalados
    Write-Host ""
    Write-Host "📋 Modelos disponibles:" -ForegroundColor Cyan
    docker exec smarteatai_ollama ollama list
    
    # Prueba rápida
    Write-Host ""
    Write-Host "🧪 Probando modelo..." -ForegroundColor Cyan
    docker exec smarteatai_ollama ollama run mistral "Hola, responde brevemente: ¿estás funcionando?"
    
    Write-Host ""
    Write-Host "✨ Ollama inicializado correctamente" -ForegroundColor Green
    Write-Host "Puedes usar el modelo 'mistral' en el backend" -ForegroundColor Green
} else {
    Write-Host "❌ Error descargando modelo" -ForegroundColor Red
    exit 1
}
