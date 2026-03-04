<h1 align="center">SmartEat AI 🥗 - Tu asistente personal de planes nutricionales personalizados</h1> 

<img width="1812" height="283" alt="image" src="https://github.com/user-attachments/assets/b512a89e-0954-41e2-8ff4-f83f52e4a789" />



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**SmartEat AI** es un proyecto de Trabajo Fin de Máster (TFM) del Curso de Especialización en Inteligencia Artificial y Big Data. Esta aplicación utiliza tecnologías de IA para proporcionar recomendaciones inteligentes sobre alimentación y nutrición.

## Índice
1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Visión y propósito](#visión-y-propósito)
3. [Características principales](#características-principales)
4. [Tecnologías utilizadas](#tecnologías-principales)
5. [Arquitectura del sistema](#estructura-general-del-proyecto)
6. [Pipeline de Ciencia de Datos](#pipeline-de-ciencia-de-datos)
7. [Aplicación Web](#aplicación-web)
8. [Instalación y despliegue](#instalación-rápida)
9. [Alcance del proyecto](#alcance-del-proyecto)
10. [Recursos utilizados](#recursos-utilizados)
11. [Autores](#autores-y--distribución-de-tareas)
12. [Licencia](#licencia)

## 1. Descripción del proyecto

SmartEat AI es una plataforma innovadora que combina inteligencia artificial y gestión nutricional para ofrecer una experiencia personalizada a los usuarios. El sistema analiza preferencias alimentarias, restricciones dietéticas y objetivos nutricionales para generar recomendaciones adaptadas a cada perfil.

En la actualidad, la planificación de una alimentación equilibrada representa un desafío para muchas personas debido a la falta de conocimiento nutricional, el tiempo limitado y la dificultad para mantener consistencia en los hábitos alimentarios. Aunque existen aplicaciones de seguimiento calórico, pocas combinan análisis inteligente, generación automática de planes y capacidad conversacional para adaptar dinámicamente la dieta del usuario.

SmartEat AI surge como respuesta a esta necesidad, proponiendo un sistema que:

- Analiza preferencias alimentarias y restricciones dietéticas.
- Tiene en cuenta objetivos nutricionales (déficit, mantenimiento, superávit).
- Genera planes semanales personalizados.
- Permite modificar dinámicamente comidas manteniendo coherencia nutricional.
- Ofrece asistencia conversacional mediante un agente inteligente.
- Modelo de Machine Learning para la recomendación en tiempo real.

Enlace al video explicatorio [click aqui]()

## 2. Visión y Propósito

El propósito de SmartEat AI es facilitar la adopción de hábitos alimenticios saludables mediante el uso de tecnología avanzada. La visión del proyecto es convertirse en una herramienta de referencia para la personalización nutricional, ayudando a los usuarios a alcanzar sus metas de bienestar de forma sencilla y efectiva.

## 3. Características Principales

- **Recomendaciones basadas en IA**: Sugerencias personalizadas de comidas y planes nutricionales.
- **Análisis nutricional**: Seguimiento detallado de macronutrientes y calorías.
- **Gestión de recetas**: Base de datos de recetas saludables.
- **Perfiles personalizados**: Configuración de objetivos y preferencias dietéticas.
- **Interfaz intuitiva**: Experiencia de usuario moderna y responsive.

## 4. Tecnologías Principales

- **Frontend**: TypeScript, Next.js, HTML5, Tailwind CSS
- **Backend**: Python, FastAPI, Base de datos relacional
- **IA & Machine Learning**: scikit-learn, joblib, LangChain, LangGraph, modelos de recomendación, procesamiento de lenguaje natural (NLP)
- **DevOps**: Docker, Docker Compose, Node 20+

## 5. Arquitectura del Sistema

### Dashboard
El dashboard desarrollado permite al usuario visualizar las comidas planificadas para el día de hoy. Cada una de ellas puede ser marcada como consumida. A medida que el usuario confirma el consumo, el sistema actualiza automáticamente las métricas nutricionales correspondientes, recalculando las calorías totales ingeridas y la distribución de macronutrientes (proteínas, hidratos de carbono y grasas), ofreciendo una visión del progreso nutricional diario.

### Profile
El Profile es la sección destinada a la gestión y configuración de la información personal y nutricional del usuario. Tras el inicio de sesión, si se trata del primer acceso a la plataforma, el sistema obliga al usuario a completar el formulario. Este proceso es necesario para garantizar la correcta personalización de los planes nutricionales.

En dicho formulario se recogen, los datos biométricos relevantes (como peso, altura, edad y sexo), así como los objetivos nutricionales (pérdida de peso, mantenimiento o ganancia de masa muscular) y el nivel de actividad física habitual. Esta información permite estimar el gasto energético y los requerimientos calóricos individuales. Adicionalmente, el usuario debe especificar sus preferencias alimentarias, incluyendo el número de comidas diarias, el tipo de dieta que desea seguir, posibles restricciones alimentarias (alergias o intolerancias) y gustos personales.

### Chat
El Chat consiste en el espacio de interacción directa con Smarty, nuestro agente virtual encargado de generar y gestionar los planes nutricionales del usuario. A través de esta interfaz, el usuario puede mantener una conversación dinámica con el sistema, permitiendo que éste genere planes personalizados basados en la información de perfil previamente proporcionada.

Además de la creación de planes, Smarty permite al usuario realizar diversas consultas y modificaciones de manera conversacional:
- Obtención del plan actual
- Visualización del perfil nutricional
- Modificación de comidas específicas dentro del plan
- Sugerencia de cambios en dichas comidas
- Buscar recetas que cumplan con las especificaciones indicadas por el usuario
- Actualizar gustos o restricciones alimentarias

### My Plan

## 6. Pipeline de Ciencia de Datos

En este apartado se describen de forma resumida los pasos realizados para preparar los datos y entrenar el modelo KNN, utilizado como recomendador de recetas. Se detalla el proceso de limpieza, transformación, etiquetado y escalado de los datos, así como la configuración y entrenamiento del modelo para garantizar recomendaciones precisas y personalizadas.

### 🎣 Obtención de los datos

Para el entrenamiento del modelo se han sacado los datos de un dataset de Kaggle.
Este dataset se obtuvo mediante webscraping de la web de [Food.com](https://www.food.com/).

[Food.com - Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews)

### 🧹 Limpieza de datos

La limpieza de datos incluyó:

- **Exploración inicial**: Identificación de valores nulos, duplicados y extremos en columnas clave.
- **Filtrado**: Eliminación de filas con valores nulos, duplicados y datos irreales (e.g., `Calories > 2000`).
- **Normalización**: Estandarización de nombres, ingredientes y valores nutricionales.
- **Etiquetado**: Clasificación en dietas (`vegan`, `vegetarian`, etc.) y tipos de comida (`breakfast`, `lunch`, etc.).

Resultado: Un dataset final de **91,056 recetas limpias**, listo para modelos de machine learning.

### 🔎 Exploración y visualización de los datos


### 📊 Preparación de los datos

La preparación de los datos incluyó:

- **Transformación**: Conversión de datos categóricos a numéricos mediante técnicas como one-hot encoding.
- **Escalado**: Normalización de valores numéricos para garantizar un rango uniforme.
- **División**: Separación del dataset en conjuntos de entrenamiento y prueba para evaluar el rendimiento del modelo.

Estos pasos aseguraron que los datos estuvieran listos para el entrenamiento del modelo KNN y otros algoritmos de machine learning.

### 🔤 Procesamiento de Lenguaje Natural

El procesamiento de lenguaje natural (NLP) se utilizó para analizar y extraer información clave de los datos textuales, como nombres de recetas e ingredientes. Estas técnicas incluyeron:

- **Tokenización**: Separación de texto en palabras clave.
- **Lematización**: Reducción de palabras a su forma base para análisis uniforme.
- **Filtrado de palabras irrelevantes**: Eliminación de stopwords y caracteres especiales.

Estas técnicas permitieron mejorar la calidad de los datos textuales y facilitar su uso en el modelo de recomendación.

### 🏋️ Entrenamiento del modelo

El modelo KNN se entrenó utilizando los datos limpios y preparados. Los pasos principales incluyeron:

- **División de datos**: Separación en conjuntos de entrenamiento y prueba.
- **Escalado**: Normalización de las características numéricas con `StandardScaler`.
- **Entrenamiento**: Uso del algoritmo KNN para ajustar el modelo a los datos de entrenamiento.

Este proceso garantizó un modelo optimizado para realizar recomendaciones precisas basadas en las preferencias y necesidades del usuario.

> Para más información sobre cada uno de los pasos descritos arriba, mirar el cuaderno `Cuaderno_SmartEatAI.ipynb` que hay en la carpeta `notebooks`.


## 7. Aplicacion Web

### 📁 Estructura General del Proyecto

```
smart-eat-ai/
├── backend/                  # Lógica de servidor, API y modelos/servicios de IA/ML
├── frontend/                 # Interfaz de usuario (Next.js)
├── docker/                   # Configuraciones de Docker
├── docker-compose.yml
├── README.md
└── LICENSE
```

> Puedes visitar la página [aquí](https://smart-eat-ai.vercel.app/)

## 8. Instalación Rápida y Despliegue

Sigue estos pasos para clonar el repositorio, instalar las dependencias y levantar los contenedores con Docker:

1. **Clona el repositorio:**
	```bash
	git clone https://github.com/SmartEatAI/smart-eat-ai.git
	cd smart-eat-ai
	```

2. **Instala las dependencias (opcional, solo si vas a desarrollar fuera de Docker):**
	- Backend:
	  ```bash
	  cd backend
	  pip install -r requirements.txt
	  ```
	- Frontend:
	  ```bash
	  cd frontend
	  npm install
	  ```
Si no funciona, ir a los README.md especificos de Backend o Frontend, que se encuentran mas desarrollados.

3. **Levanta los contenedores con Docker:**
	```bash
	docker compose build
	docker compose up
	```

4. **Accede a la aplicación:**
	- Frontend: [http://localhost:3000](http://localhost:3000)
	- Backend API: [http://localhost:8000](http://localhost:8000)
	- Documentación API: [http://localhost:8000/docs](http://localhost:8000/docs)


## 9. Alcance del Proyecto

SmartEat AI está diseñado como una solución integral para la gestión nutricional personalizada. El proyecto abarca desde la recolección y análisis de datos de usuario, hasta la generación de recomendaciones y la visualización de información relevante en una interfaz moderna. El alcance incluye la integración de modelos de IA, la gestión de recetas y perfiles, y la provisión de una experiencia accesible tanto para usuarios finales como para profesionales de la nutrición.

## 10. Recursos utilizados
- [Documentación Ollama, métricas de modelos](https://ollama.com/)
- [Documentación LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [Documentación LangChain](https://docs.langchain.com/oss/python/langchain/overview)
- [Documentación ShadCN](https://ui.shadcn.com/docs)
- [Curso de Introducción a #FastAPI 2025 - #Backend con #Python](https://youtube.com/playlist?list=PLHftsZss8mw7pSRpCyd-TM4Mu43XdyB3R&si=EWsPmgy1PdGROFaU)
- [Tutorial LangGraph](https://www.youtube.com/watch?v=LS4pALyrm00)
- [Tutorial LangChain](https://www.youtube.com/watch?v=HUcIxt1v0wU)
- [ChatGPT](https://chatgpt.com/)
- [DeepSeek](https://chat.deepseek.com/)

## 11. Autores y Distribución de tareas

- [Elías Robles Ruíz](https://github.com/eliasrrobles) - 33.33%
- [Cristina Vacas López](https://github.com/flashtime-dev) - 33.33%
- [Ruyi Xia Ye](https://github.com/rxy94) - 33.33%
- 

## 12. Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
⭐ Si te gusta este proyecto, danos una estrellita en GitHub!
