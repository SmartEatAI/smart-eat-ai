<h1 align="center">SmartEat AI 🥗 - Tu asistente personal de planes nutricionales personalizados</h1> 

<img width="1812" height="283" alt="image" src="https://github.com/user-attachments/assets/b512a89e-0954-41e2-8ff4-f83f52e4a789" />



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**SmartEat AI** es un proyecto de Trabajo Fin de Máster (TFM) del Curso de Especialización en Inteligencia Artificial y Big Data. Esta aplicación utiliza tecnologías de IA para proporcionar recomendaciones inteligentes sobre alimentación y nutrición.

> [Presentación del proyecto](https://www.canva.com/design/DAHCnfU5p6s/D2NN2HH-_N1PsZlCq9sJpg/view?utm_content=DAHCnfU5p6s&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h708a869ec2)
>
> [Video explicatorio]()
>
> [App desplegada](https://smart-eat-ai.vercel.app/)
> 
> [Documentación](https://smarteatai-smart-eat-ai.mintlify.app/)

## Índice
1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Visión y propósito](#2-visión-y-propósito)
3. [Características principales](#3-características-principales)
4. [Tecnologías utilizadas](#4-tecnologías-principales)
5. [Arquitectura del sistema](#5-arquitectura-del-sistema)
6. [Pipeline de Ciencia de Datos](#6-pipeline-de-ciencia-de-datos)
7. [Aplicación Web](#7-aplicacion-web)
8. [Instalación y despliegue](#8-instalación-rápida-y-despliegue)
9. [Alcance del proyecto](#9-alcance-del-proyecto)
10. [Recursos utilizados](#10-recursos-utilizados)
11. [Autores](#11-autores-y-distribución-de-tareas)
12. [Licencia](#12-licencia)

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

![Arquitectura](/img/arquitectura-smarteatai.png)

## 6. Pipeline de Ciencia de Datos

En este apartado se describen de forma resumida los pasos realizados para preparar los datos y entrenar el modelo KNN, utilizado como recomendador de recetas. Se detalla el proceso de limpieza, transformación, etiquetado y escalado de los datos, así como la configuración y entrenamiento del modelo para garantizar recomendaciones precisas y personalizadas.

### 🎣 Obtención de los datos

Para el entrenamiento del modelo se han sacado los datos de un dataset de Kaggle.
Este dataset se obtuvo mediante webscraping de la web de [Food.com](https://www.food.com/).

[Food.com - Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews)


### 🔎 Exploración y visualización de los datos

#### Información general del dataset

Tiene 522517 recetas (filas) y 28 columnas.

| Columna                      | Tipo    | Nulos   | Descripción                                         |
| ---------------------------- | ------- | ------- | --------------------------------------------------- |
| `RecipeId`                   | int64   | 0       | Identificador único de la receta                    |
| `Name`                       | object  | 0       | Nombre de la receta                                 |
| `AuthorId`                   | int64   | 0       | Identificador único del autor                       |
| `AuthorName`                 | object  | 0       | Nombre del autor de la receta                       |
| `CookTime`                   | object  | 82.545  | Tiempo de cocción (formato texto, p. ej. ISO 8601)  |
| `PrepTime`                   | object  | 0       | Tiempo de preparación de la receta                  |
| `TotalTime`                  | object  | 0       | Tiempo total de elaboración                         |
| `DatePublished`              | object  | 0       | Fecha de publicación de la receta                   |
| `Description`                | object  | 5       | Descripción textual de la receta                    |
| `Images`                     | object  | 1       | Enlaces o metadatos de imágenes asociadas           |
| `RecipeCategory`             | object  | 751     | Categoría culinaria de la receta                    |
| `Keywords`                   | object  | 17.237  | Palabras clave o etiquetas                          |
| `RecipeIngredientQuantities` | object  | 3       | Cantidades de los ingredientes (texto estructurado) |
| `RecipeIngredientParts`      | object  | 0       | Lista de ingredientes de la receta                  |
| `AggregatedRating`           | float64 | 253.223 | Valoración media de la receta                       |
| `ReviewCount`                | float64 | 247.489 | Número de reseñas                                   |
| `Calories`                   | float64 | 0       | Calorías totales de la receta                       |
| `FatContent`                 | float64 | 0       | Contenido total de grasa (g)                        |
| `SaturatedFatContent`        | float64 | 0       | Contenido de grasas saturadas (g)                   |
| `CholesterolContent`         | float64 | 0       | Contenido de colesterol (mg)                        |
| `SodiumContent`              | float64 | 0       | Contenido de sodio (mg)                             |
| `CarbohydrateContent`        | float64 | 0       | Contenido total de carbohidratos (g)                |
| `FiberContent`               | float64 | 0       | Contenido de fibra (g)                              |
| `SugarContent`               | float64 | 0       | Contenido de azúcares (g)                           |
| `ProteinContent`             | float64 | 0       | Contenido de proteínas (g)                          |
| `RecipeServings`             | float64 | 182.911 | Número de porciones                                 |
| `RecipeYield`                | object  | 348.071 | Rendimiento de la receta (texto libre)              |
| `RecipeInstructions`         | object  | 0       | Instrucciones paso a paso de la receta              |

#### Exploración de nulos
![heatmap_valores_nulos](/img/heatmap_valores_nulos.png)

#### Exploración de duplicados
Se identificaron recetas con nombres repetidos en el dataset; se inspeccionaron y trataron (eliminación o consolidación) para evitar duplicidad en el conjunto final.

#### Resumen estadístico

<div id="df-5f113fac-dfa4-4346-8697-d88b702d547a" class="colab-df-container">
    <div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>RecipeId</th>
      <th>AuthorId</th>
      <th>AggregatedRating</th>
      <th>ReviewCount</th>
      <th>Calories</th>
      <th>FatContent</th>
      <th>SaturatedFatContent</th>
      <th>CholesterolContent</th>
      <th>SodiumContent</th>
      <th>CarbohydrateContent</th>
      <th>FiberContent</th>
      <th>SugarContent</th>
      <th>ProteinContent</th>
      <th>RecipeServings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>522517.000000</td>
      <td>5.225170e+05</td>
      <td>269294.000000</td>
      <td>275028.000000</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>5.225170e+05</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>522517.000000</td>
      <td>339606.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>271821.436970</td>
      <td>4.572585e+07</td>
      <td>4.632014</td>
      <td>5.227784</td>
      <td>484.438580</td>
      <td>24.614922</td>
      <td>9.559457</td>
      <td>86.487003</td>
      <td>7.672639e+02</td>
      <td>49.089092</td>
      <td>3.843242</td>
      <td>21.878254</td>
      <td>17.469510</td>
      <td>8.606191</td>
    </tr>
    <tr>
      <th>std</th>
      <td>155495.878422</td>
      <td>2.929714e+08</td>
      <td>0.641934</td>
      <td>20.381347</td>
      <td>1397.116649</td>
      <td>111.485798</td>
      <td>46.622621</td>
      <td>301.987009</td>
      <td>4.203621e+03</td>
      <td>180.822062</td>
      <td>8.603163</td>
      <td>142.620191</td>
      <td>40.128837</td>
      <td>114.319809</td>
    </tr>
    <tr>
      <th>min</th>
      <td>38.000000</td>
      <td>2.700000e+01</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>137206.000000</td>
      <td>6.947400e+04</td>
      <td>4.500000</td>
      <td>1.000000</td>
      <td>174.200000</td>
      <td>5.600000</td>
      <td>1.500000</td>
      <td>3.800000</td>
      <td>1.233000e+02</td>
      <td>12.800000</td>
      <td>0.800000</td>
      <td>2.500000</td>
      <td>3.500000</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>271758.000000</td>
      <td>2.389370e+05</td>
      <td>5.000000</td>
      <td>2.000000</td>
      <td>317.100000</td>
      <td>13.800000</td>
      <td>4.700000</td>
      <td>42.600000</td>
      <td>3.533000e+02</td>
      <td>28.200000</td>
      <td>2.200000</td>
      <td>6.400000</td>
      <td>9.100000</td>
      <td>6.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>406145.000000</td>
      <td>5.658280e+05</td>
      <td>5.000000</td>
      <td>4.000000</td>
      <td>529.100000</td>
      <td>27.400000</td>
      <td>10.800000</td>
      <td>107.900000</td>
      <td>7.922000e+02</td>
      <td>51.100000</td>
      <td>4.600000</td>
      <td>17.900000</td>
      <td>25.000000</td>
      <td>8.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>541383.000000</td>
      <td>2.002886e+09</td>
      <td>5.000000</td>
      <td>3063.000000</td>
      <td>612854.600000</td>
      <td>64368.100000</td>
      <td>26740.600000</td>
      <td>130456.400000</td>
      <td>1.246921e+06</td>
      <td>108294.600000</td>
      <td>3012.000000</td>
      <td>90682.300000</td>
      <td>18396.200000</td>
      <td>32767.000000</td>
    </tr>
  </tbody>
</table>
</div>

#### Distribución de recetas por número de ingredientes

![Distribución de recetas por número de ingredientes](/img/distribucion_de_recetas_por_numero_de_ingredientes.png)

#### Análisis nutricional

Distribución de macronutrientes con histogramas de:

- calories
- fat
- protein
- carbohydrates

![Análisis nutricional](/img/analisis_nutricional.png)

![Análisis nutricional logaritmico](/img/analisis_nutricional_logaritmico.png)

Relación entre macronutrientes con scatter plots de:

- calories vs protein
- calories vs fat
- fat vs carbohydrates

![Análisis nutricional scatter](/img/relacion_entre_macronutrientes.png)

#### Análisis de ingredientes

Frecuencia de ingredientes con Barplot top-40 ingredientes

Número de ingredientes vs nutrición con Scatter:

- n_ingredients vs calories
- n_ingredients vs fat

![Top 40 de ingredientes más frecuentes](/img/top40_ingredientes_mas_frecuentes.png)

![Número de ingredientes vs macros](/img/numero_ingredientes_vs_macros.png)

#### Analisis de tags y categorias dieteticas

Frecuencia de tags con Barplot top-30 tags y Wordcloud

![Top 30 de Keywords más frecuentes](/img/top30_keywords_mas_frecuentes.png)

![Nube de palabras: Keywords de Recetas](/img/wordcloud_keywords_mas_frecuentes.png)

Frecuencia de tags con Barplot top-50 tags

![Top-50 Categorias más frecuentes](/img/top50_categorias_mas_frecuentes.png)

Nutrición por tipo de dieta con boxplots de:

- calorias por tipo de dieta
- proteina por tipo de dieta

![Comparativa de Calorías por Tipo de Dieta](/img/comparativa_de_calorias_diet_type.png)


### 🧹 Limpieza de datos

La limpieza de datos incluyó:

- **Exploración inicial**: Identificación de valores nulos, duplicados y extremos en columnas clave.
- **Filtrado**: Eliminación de filas con valores nulos, duplicados y datos irreales (e.g., `Calories > 2000`).
- **Normalización**: Estandarización de nombres, ingredientes y valores nutricionales.
- **Etiquetado**: Clasificación en dietas (`vegan`, `vegetarian`, etc.) y tipos de comida (`breakfast`, `lunch`, etc.).

Resultado: Un dataset final de **91,056 recetas limpias**, listo para modelos de machine learning.

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

La aplicacion esta dividida en 4 modulos principales:

### Dashboard
El dashboard desarrollado permite al usuario visualizar las comidas planificadas para el día de hoy. Cada una de ellas puede ser marcada como consumida. A medida que el usuario confirma el consumo, el sistema actualiza automáticamente las métricas nutricionales correspondientes, recalculando las calorías totales ingeridas y la distribución de macronutrientes (proteínas, hidratos de carbono y grasas), ofreciendo una visión del progreso nutricional diario.
<img width="1553" height="875" alt="Captura de pantalla 2026-03-03 204642" src="https://github.com/user-attachments/assets/c63ddd5e-d91b-4abf-b190-25eb4ea4355b" />

### Profile
El Profile es la sección destinada a la gestión y configuración de la información personal y nutricional del usuario. Tras el inicio de sesión, si se trata del primer acceso a la plataforma, el sistema obliga al usuario a completar el formulario. Este proceso es necesario para garantizar la correcta personalización de los planes nutricionales.

En dicho formulario se recogen, los datos biométricos relevantes (como peso, altura, edad y sexo), así como los objetivos nutricionales (pérdida de peso, mantenimiento o ganancia de masa muscular) y el nivel de actividad física habitual. Esta información permite estimar el gasto energético y los requerimientos calóricos individuales. Adicionalmente, el usuario debe especificar sus preferencias alimentarias, incluyendo el número de comidas diarias, el tipo de dieta que desea seguir, posibles restricciones alimentarias (alergias o intolerancias) y gustos personales.
<img width="1586" height="899" alt="Captura de pantalla 2026-03-03 204838" src="https://github.com/user-attachments/assets/8b05c0b8-f5d0-4a53-8e33-31c823e6af32" />

### Chat
El Chat consiste en el espacio de interacción directa con Smarty, nuestro agente virtual encargado de generar y gestionar los planes nutricionales del usuario. A través de esta interfaz, el usuario puede mantener una conversación dinámica con el sistema, permitiendo que éste genere planes personalizados basados en la información de perfil previamente proporcionada.

Además de la creación de planes, Smarty permite al usuario realizar diversas consultas y modificaciones de manera conversacional:
- Obtención del plan actual
- Visualización del perfil nutricional
- Modificación de comidas específicas dentro del plan
- Sugerencia de cambios en dichas comidas
- Buscar recetas que cumplan con las especificaciones indicadas por el usuario
- Actualizar gustos o restricciones alimentarias
<img width="1616" height="901" alt="Captura de pantalla 2026-03-04 110546" src="https://github.com/user-attachments/assets/9974e1a9-d7ea-4e59-8eb0-b5cbf0d9b5a7" />

### My Plan
El modulo de my plan es un espacio de visualización y gestión del plan nutricional actual del usuario. En esta sección, se presentan estadísticas detalladas sobre el consumo medio de calorías y macronutrientes a lo largo de la semana.

Cada receta incluida en los menús diarios se muestra de forma individual, ofreciendo al usuario la posibilidad de realizar modificaciones directamente sobre las comidas programadas. Específicamente, el sistema permite realizar un swap en cualquier comida, aceptando la sugerencia propuesta por la plataforma, solicitando una alternativa adicional o rechazando la modificación para mantener la comida original. Dicho swap es recomendado por nuestro modelo KNN entrenado anteriorne.
<img width="1584" height="857" alt="Captura de pantalla 2026-03-03 204808" src="https://github.com/user-attachments/assets/ea46a9b3-8f86-4b9b-96f0-b9eae3cbb827" />

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

## 12. Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
⭐ Si te gusta este proyecto, danos una estrellita en GitHub!
