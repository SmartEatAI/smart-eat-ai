"""
Servicio para interactuar con el modelo KNN de recomendación de recetas.
Gestiona la carga del modelo y búsqueda de recetas similares por distancia euclidiana.
"""

import pickle
import joblib
from typing import List, Tuple, Optional
from functools import lru_cache
import numpy as np
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.models.modelo_ml_metadata import ModeloMLMetadata
import logging

logger = logging.getLogger(__name__)


class KNNService:
    """Singleton service para gestionar el modelo KNN"""
    
    _instance = None
    _model = None
    _scaler = None
    _feature_columns = None
    _model_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KNNService, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def load_model(cls, model_path: str, scaler_path: Optional[str] = None, 
                   feature_columns: Optional[List[str]] = None):
        """
        Carga el modelo KNN y el scaler desde archivos pickle/joblib.
        
        Args:
            model_path: Ruta al archivo .pkl del modelo KNN
            scaler_path: Ruta al archivo .pkl del scaler (opcional)
            feature_columns: Lista de columnas de features en orden correcto
        """
        try:
            # Intentar cargar con joblib primero, fallback a pickle
            try:
                cls._model = joblib.load(model_path)
                logger.info(f"Modelo KNN cargado exitosamente desde {model_path}")
            except:
                with open(model_path, 'rb') as f:
                    cls._model = pickle.load(f)
                logger.info(f"Modelo KNN cargado con pickle desde {model_path}")
            
            # Cargar scaler si existe
            if scaler_path:
                try:
                    cls._scaler = joblib.load(scaler_path)
                    logger.info(f"Scaler cargado desde {scaler_path}")
                except:
                    with open(scaler_path, 'rb') as f:
                        cls._scaler = pickle.load(f)
                    logger.info(f"Scaler cargado con pickle desde {scaler_path}")
            
            cls._feature_columns = feature_columns or [
                'calorias', 'proteinas', 'carbohidratos', 'grasas'
            ]
            cls._model_loaded = True
            logger.info(f"Modelo KNN inicializado con features: {cls._feature_columns}")
            
        except Exception as e:
            logger.error(f"Error cargando modelo KNN: {e}")
            cls._model_loaded = False
            raise
    
    @classmethod
    def is_loaded(cls) -> bool:
        """Verifica si el modelo está cargado"""
        return cls._model_loaded
    
    @classmethod
    @lru_cache(maxsize=1000)
    def get_feature_vector(cls, receta_id: int, db: Session) -> np.ndarray:
        """
        Extrae y normaliza el vector de features de una receta.
        Cache para evitar queries repetidas.
        
        Args:
            receta_id: ID de la receta
            db: Sesión de base de datos
            
        Returns:
            Vector numpy con features normalizados
        """
        if not cls._model_loaded:
            raise RuntimeError("Modelo KNN no está cargado. Llamar a load_model() primero.")
        
        # TODO: Implementar query a BD
        receta = db.query(Receta).filter(Receta.id == receta_id).first()
        if not receta:
            raise ValueError(f"Receta {receta_id} no encontrada")
        
        # Extraer features según columnas definidas
        features = []
        for col in cls._feature_columns:
            value = getattr(receta, col, 0.0)
            features.append(float(value) if value is not None else 0.0)
        
        features_array = np.array(features).reshape(1, -1)
        
        # Aplicar scaler si existe
        if cls._scaler:
            features_array = cls._scaler.transform(features_array)
        
        return features_array
    
    @classmethod
    def find_similar_recipes(
        cls, 
        receta_id: int, 
        db: Session,
        k: int = 5, 
        exclude_recipe_ids: Optional[List[int]] = None
    ) -> List[Tuple[int, float]]:
        """
        Encuentra las k recetas más similares usando el modelo KNN.
        
        Args:
            receta_id: ID de la receta de referencia
            db: Sesión de base de datos
            k: Número de vecinos a retornar
            exclude_recipe_ids: IDs de recetas a excluir (ej: ya en el plan)
            
        Returns:
            Lista de tuplas (receta_id, distancia) ordenadas por similitud
        """
        if not cls._model_loaded:
            raise RuntimeError("Modelo KNN no está cargado")
        
        # TODO: Implementar lógica completa
        # 1. Obtener vector de features de la receta
        feature_vector = cls.get_feature_vector(receta_id, db)
        
        # 2. Consultar modelo KNN
        # distances, indices = cls._model.kneighbors(feature_vector, n_neighbors=k+1)
        
        # 3. Filtrar receta original y recetas excluidas
        # exclude_set = set(exclude_recipe_ids or [])
        # exclude_set.add(receta_id)
        
        # 4. Retornar resultados
        logger.warning("find_similar_recipes: Implementación pendiente")
        return []
    
    @classmethod
    def get_model_info(cls, db: Session) -> Optional[dict]:
        """
        Obtiene información del modelo activo desde la BD.
        
        Returns:
            Dict con metadata del modelo o None
        """
        # TODO: Query a ModeloMLMetadata para obtener versión activa
        if not cls._model_loaded:
            return None
        
        return {
            "loaded": cls._model_loaded,
            "feature_columns": cls._feature_columns,
            "has_scaler": cls._scaler is not None
        }
