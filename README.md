# SmartEat AI

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

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

**SmartEatAI Team**
- [Elías Robles Ruíz](https://github.com/eliasrrobles)
- [Cristina Vacas López](https://github.com/flashtime-dev)
- [Ruyi Xia Ye](https://github.com/rxy94)

---
⭐ Si te gusta este proyecto, danos una estrellita en GitHub!