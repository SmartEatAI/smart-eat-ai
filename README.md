<center>
<h1>SmartEat AI</h1>
	
<img src="https://images.emojiterra.com/google/android-12l/512px/1f957.png" alt="Logo" width="400">
</center>



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**SmartEat AI** es un proyecto de Trabajo Fin de Máster (TFM) del Curso de Especialización en Inteligencia Artificial y Big Data. Esta aplicación utiliza tecnologías de IA para proporcionar recomendaciones inteligentes sobre alimentación y nutrición.

## 📋 Descripción General

SmartEat AI es una plataforma innovadora que combina inteligencia artificial y gestión nutricional para ofrecer una experiencia personalizada a los usuarios. El sistema analiza preferencias alimentarias, restricciones dietéticas y objetivos nutricionales para generar recomendaciones adaptadas a cada perfil.

## 🌟 Visión y Propósito

El propósito de SmartEat AI es facilitar la adopción de hábitos alimenticios saludables mediante el uso de tecnología avanzada. La visión del proyecto es convertirse en una herramienta de referencia para la personalización nutricional, ayudando a los usuarios a alcanzar sus metas de bienestar de forma sencilla y efectiva.

## 🚀 Características Principales

- **Recomendaciones basadas en IA**: Sugerencias personalizadas de comidas y planes nutricionales.
- **Análisis nutricional**: Seguimiento detallado de macronutrientes y calorías.
- **Gestión de recetas**: Base de datos de recetas saludables.
- **Perfiles personalizados**: Configuración de objetivos y preferencias dietéticas.
- **Interfaz intuitiva**: Experiencia de usuario moderna y responsive.

## 🛠️ Tecnologías Principales

- **Frontend**: TypeScript, Next.js, HTML5, Tailwind CSS
- **Backend**: Python, FastAPI, Base de datos relacional
- **IA & Machine Learning**: scikit-learn, joblib, LangChain, LangGraph, modelos de recomendación, procesamiento de lenguaje natural (NLP)
- **DevOps**: Docker, Docker Compose, Node 20+

## 📁 Estructura General del Proyecto

```
smart-eat-ai/
├── backend/                  # Lógica de servidor, API y modelos/servicios de IA/ML
├── frontend/                 # Interfaz de usuario (Next.js)
├── docker/                   # Configuraciones de Docker
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 🚀 Instalación Rápida

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


## 📦 Alcance del Proyecto

SmartEat AI está diseñado como una solución integral para la gestión nutricional personalizada. El proyecto abarca desde la recolección y análisis de datos de usuario, hasta la generación de recomendaciones y la visualización de información relevante en una interfaz moderna. El alcance incluye la integración de modelos de IA, la gestión de recetas y perfiles, y la provisión de una experiencia accesible tanto para usuarios finales como para profesionales de la nutrición.

## 📚 Recursos utilizados
- [Documentación Ollama, métricas de modelos](https://ollama.com/)
- [Documentación LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [Documentación LangChain](https://docs.langchain.com/oss/python/langchain/overview)
- [Documentación ShadCN](https://ui.shadcn.com/docs)
- [Curso de Introducción a #FastAPI 2025 - #Backend con #Python](https://youtube.com/playlist?list=PLHftsZss8mw7pSRpCyd-TM4Mu43XdyB3R&si=EWsPmgy1PdGROFaU)
- [Tutorial LangGraph](https://www.youtube.com/watch?v=LS4pALyrm00)
- [Tutorial LangChain](https://www.youtube.com/watch?v=HUcIxt1v0wU)
- [ChatGPT](https://chatgpt.com/)
- [DeepSeek](https://chat.deepseek.com/)

## 👥 Autores y ⚖️ Distribución de tareas

- [Elías Robles Ruíz](https://github.com/eliasrrobles) - 33.33%
- [Cristina Vacas López](https://github.com/flashtime-dev) - 33.33%
- [Ruyi Xia Ye](https://github.com/rxy94) - 33.33%
- 

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
⭐ Si te gusta este proyecto, danos una estrellita en GitHub!
