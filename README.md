# SmartEat AI

![License:  MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**SmartEat AI** es un proyecto de Trabajo Fin de Máster (TFM) del Curso de Especialización en Inteligencia Artificial y Big Data.  Esta aplicación utiliza tecnologías de IA para proporcionar recomendaciones inteligentes sobre alimentación y nutrición.

## 📋 Descripción

SmartEat AI es una plataforma que combina inteligencia artificial con gestión nutricional para ofrecer una experiencia personalizada a los usuarios. El sistema analiza preferencias alimentarias, restricciones dietéticas y objetivos nutricionales para proporcionar recomendaciones personalizadas.

## 🚀 Características

- **Recomendaciones basadas en IA**: Sugerencias personalizadas de comidas y planes nutricionales
- **Análisis nutricional**: Seguimiento detallado de macronutrientes y calorías
- **Gestión de recetas**: Base de datos de recetas saludables
- **Perfiles personalizados**: Configuración de objetivos y preferencias dietéticas
- **Interfaz intuitiva**: Experiencia de usuario moderna y responsive

## 🛠️ Tecnologías

### Frontend
- JavaScript
- React
- HTML5 & Tailwind CSS

### Backend
- Python
- FastAPI
- Base de datos [Especificar: MongoDB, PostgreSQL, MySQL, etc.]

### IA & Machine Learning
- [Especificar:  TensorFlow, PyTorch, scikit-learn, etc.]
- Modelos de recomendación
- Procesamiento de lenguaje natural (NLP)

### DevOps
- Docker & Docker Compose

## 📁 Estructura del Proyecto

```
smart-eat-ai/
├── backend/          # Código del servidor, API y lógica de IA/ML
├── frontend/         # Interfaz de usuario (React)
│   └── components/   # Componentes React
│       ├── layout/   # Componentes estructurales globales (Header, Footer, etc.)
│       ├── ui/       # Componentes reutilizables y genéricos
│       └── features/ # Componentes agrupados por funcionalidad o vista
├── docker/           # Configuraciones de Docker
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 🔧 Instalación y Configuración

### Requisitos Previos

- Docker y Docker Compose instalados

### Instalación con Docker

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/SmartEatAI/smart-eat-ai.git
   cd smart-eat-ai
   ```

2. **Construir las imágenes e iniciar los contenedores**
   ```bash
   docker compose build
   docker compose up
   ```

3. **Acceder a la aplicación**
   - Frontend: `http://localhost:3000`
   - Backend API:
     ```bash
      http://localhost:8000
      http://localhost:8000/health
      http://localhost:8000/docs
      ```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

**SmartEatAI Team**
- [Elías Robles Ruíz](https://github.com/eliasrrobles)
- [Cristina Vacas López](https://github.com/flashtime-dev)
- [Ruyi Xia Ye](https://github.com/rxy94)

---

⭐ Si te gusta este proyecto, danos una estrellita en GitHub!