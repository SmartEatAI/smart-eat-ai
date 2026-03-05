# Notebooks

Este directorio contiene notebooks Jupyter usados para exploración, generación de la base de datos vectorial y pruebas de modelos del proyecto Smart-Eat-AI.

Contenido principal
- `Cuaderno_SmartEatAI.ipynb` — Notebook principal con experimentos, visualizaciones y notas generales.
- `generar_base_de_datos_vectorial.ipynb` — Notebook para generar la base de datos vectorial (Chroma/FAISS u otra) usada en el buscador/recomendador.

Cómo abrir
- Desde la raíz del proyecto, inicia Jupyter Lab/Notebook en el entorno Python apropiado:

```bash
# conda
conda activate <tu-entorno>
jupyter lab

# o con venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
jupyter lab
```

Ejecutar notebooks (headless)

```bash
jupyter nbconvert --to notebook --execute notebooks/generar_base_de_datos_vectorial.ipynb --output executed.ipynb
```

Dependencias y entorno
- Usa el mismo entorno Python que el backend; revisa `backend/requirements.txt` y `docker/backend/requirements.txt`.
- Si los notebooks usan artefactos (modelos, vectores), comprueba `backend/files/` y `backend/data/`.

Notas útiles
- Mantén copias de los notebooks importantes (no ejecutar directamente en producción sin revisar).
- Para reproducibilidad, documenta en los notebooks las versiones de paquetes (ej. `pip freeze > requirements.txt`).

Soporte
- Para más detalles consulta el README principal en la raíz del repositorio.
