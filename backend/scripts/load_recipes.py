"""
Script de ejemplo para cargar recetas desde CSV/JSON al sistema.
Incluye generación de embeddings para búsqueda semántica.

Uso:
    python scripts/load_recipes.py --input data/recetas.csv --format csv
"""

import argparse
import json
import pandas as pd
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.receta import Receta
from app.models.embedding_receta import EmbeddingReceta


def load_embedding_model():
    """Carga el modelo de embeddings"""
    print("📥 Cargando modelo de embeddings all-MiniLM-L6-v2...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("✅ Modelo cargado")
    return model


def generate_recipe_text(receta_data: dict) -> str:
    """
    Genera texto descriptivo de una receta para embedding.
    Combina nombre y características nutricionales.
    """
    parts = [receta_data['nombre']]
    
    # Añadir características nutricionales principales
    nutri = f"Calorías: {receta_data.get('calorias', 0)}, "
    nutri += f"Proteínas: {receta_data.get('proteinas', 0)}g, "
    nutri += f"Carbohidratos: {receta_data.get('carbohidratos', 0)}g, "
    nutri += f"Grasas: {receta_data.get('grasas', 0)}g"
    parts.append(nutri)
    
    return ' '.join(parts)


def load_from_csv(file_path: str) -> list:
    """Carga recetas desde archivo CSV"""
    print(f"📄 Leyendo CSV: {file_path}")
    df = pd.read_csv(file_path)
    
    # Convertir DataFrame a lista de diccionarios
    recetas = df.to_dict('records')
    print(f"✅ {len(recetas)} recetas encontradas")
    
    return recetas


def load_from_json(file_path: str) -> list:
    """Carga recetas desde archivo JSON"""
    print(f"📄 Leyendo JSON: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        recetas = json.load(f)
    
    if isinstance(recetas, dict) and 'recetas' in recetas:
        recetas = recetas['recetas']
    
    print(f"✅ {len(recetas)} recetas encontradas")
    return recetas


def insert_recipes(recetas: list, db: Session, embedding_model):
    """
    Inserta recetas en la base de datos con sus embeddings.
    """
    print(f"\n💾 Insertando {len(recetas)} recetas en la base de datos...")
    
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, receta_data in enumerate(recetas, 1):
        try:
            # Verificar si ya existe
            nombre = receta_data.get('nombre')
            if db.query(Receta).filter(Receta.nombre == nombre).first():
                print(f"⚠️  [{idx}/{len(recetas)}] Receta '{nombre}' ya existe, omitiendo...")
                skipped_count += 1
                continue
            
            # Crear objeto Receta
            receta = Receta(
                nombre=receta_data.get('nombre'),
                calorias=int(receta_data.get('calorias', 0)),
                proteinas=int(receta_data.get('proteinas', 0)),
                carbohidratos=int(receta_data.get('carbohidratos', 0)),
                grasas=int(receta_data.get('grasas', 0)),
                url_imagen=receta_data.get('url_imagen'),
                url_receta=receta_data.get('url_receta')
            )
            
            db.add(receta)
            db.flush()  # Para obtener el ID
            
            # Generar embedding
            texto_embedding = generate_recipe_text(receta_data)
            embedding_vector = embedding_model.encode(texto_embedding)
            
            # Guardar embedding
            embedding = EmbeddingReceta(
                receta_id=receta.id,
                embedding=embedding_vector.tolist(),
                modelo_version="all-MiniLM-L6-v2"
            )
            db.add(embedding)
            
            inserted_count += 1
            
            if idx % 10 == 0:
                print(f"✅ [{idx}/{len(recetas)}] Procesadas...")
            
        except Exception as e:
            print(f"❌ Error procesando receta {idx}: {e}")
            error_count += 1
            db.rollback()
            continue
    
    # Commit final
    try:
        db.commit()
        print(f"\n✨ Proceso completado:")
        print(f"   ✅ Insertadas: {inserted_count}")
        print(f"   ⚠️  Omitidas: {skipped_count}")
        print(f"   ❌ Errores: {error_count}")
    except Exception as e:
        print(f"❌ Error en commit final: {e}")
        db.rollback()


def main():
    parser = argparse.ArgumentParser(description='Carga recetas al sistema SmartEat AI')
    parser.add_argument('--input', required=True, help='Ruta al archivo de recetas')
    parser.add_argument('--format', choices=['csv', 'json'], required=True, help='Formato del archivo')
    
    args = parser.parse_args()
    
    # Verificar archivo existe
    if not os.path.exists(args.input):
        print(f"❌ Archivo no encontrado: {args.input}")
        return
    
    # Cargar recetas
    if args.format == 'csv':
        recetas = load_from_csv(args.input)
    else:
        recetas = load_from_json(args.input)
    
    # Cargar modelo de embeddings
    embedding_model = load_embedding_model()
    
    # Conectar a BD
    print("\n🔌 Conectando a base de datos...")
    db = SessionLocal()
    
    try:
        insert_recipes(recetas, db, embedding_model)
    finally:
        db.close()
        print("\n🔒 Conexión cerrada")


if __name__ == "__main__":
    main()
