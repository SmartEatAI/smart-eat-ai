# 🦙 SmartEatAI: Agente IA con Llama 3 + Nomic Embeddings (Docker)

Este proyecto implementa un agente conversacional con arquitectura RAG
(Retrieval-Augmented Generation) utilizando modelos ejecutados
localmente mediante Ollama dentro de Docker.

------------------------------------------------------------------------

# 🐳 Uso con Docker

## Construir la imagen y contenedores

Desde la raiz del proyecto ejecutar

``` bash
docker compose up
```

------------------------------------------------------------------------

# 🚀 Modelos Necesarios

Antes de hacer uso debemos estar dentro del contenedor de ollama y descargar los siguientes modelos:

## 🔹 Llama 3 y Llama 3.1

``` bash
ollama pull llama3
```

``` bash
ollama pull llama3.1
```

## 🔹 Modelo de embeddings

``` bash
ollama pull nomic-embed-text
```

------------------------------------------------------------------------

# 📦 Dependencias

El contenedor incluye:

-   Python 3.10+
-   LangChain
-   Ollama client
-   ChromaDB
-   FastAPI + Uvicorn

------------------------------------------------------------------------

# 🧠 Arquitectura del Agente

1.  Usuario envía pregunta
2.  Se generan embeddings con `nomic-embed-text`
3.  Se realiza búsqueda vectorial
4.  Se construye contexto
5.  Se envía prompt enriquecido a `llama3` o `llama3.1`
6.  Se devuelve respuesta final

------------------------------------------------------------------------

# 🔎 Verificar modelos instalados

Dentro del contenedor o en el host:

``` bash
ollama list
```

------------------------------------------------------------------------

# ⚠️ Problemas Comunes

## ❌ Error: model not found

Ejecutar nuevamente:

``` bash
ollama pull llama3
ollama pull nomic-embed-text
```

## ❌ Error: connection refused

Asegurarse de que Ollama esté corriendo:

``` bash
ollama serve
```

------------------------------------------------------------------------

# 🪅 Obtener la ChromaDB

* Abre el archivo de `generar_base_de_datos_vectorial.ipynb`.

* Crea un venv.

``` bash
python -m venv venv
```

* Instala las dependencias y ejecutalo.

* Una vez tengas la carpeta colocala en `/backend/app/data/`, tras eso ya podrás hacer uso del modelo y demás características de la aplicación.

------------------------------------------------------------------------

# 📌 Notas

-   Los modelos se ejecutan completamente en local.
-   No se envían datos a servicios externos.
-   El rendimiento depende directamente del hardware disponible.
