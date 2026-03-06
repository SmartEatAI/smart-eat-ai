"""
Utilidades para manejar rate limits de Groq en las tools del agente.

Groq tiene límites estrictos en el plan gratuito:
- 30 requests/minuto
- 6,000 tokens/minuto
- 14,400 requests/día

Este módulo proporciona funciones para:
1. Validar múltiples recetas en una sola llamada (batch)
2. Implementar backoff exponencial para rate limits
"""
import logging
import time
from typing import List, Dict, Any, Optional
from groq import RateLimitError

logger = logging.getLogger(__name__)

# Configuración de rate limiting
MAX_RETRIES = 3
BASE_WAIT_TIME = 2  # segundos


def validate_recipes_batch(
    llm,
    recipes: List[Any],
    restrictions_text: str,
    diet_text: str = "",
    batch_size: int = 10
) -> List[Any]:
    """
    Valida múltiples recetas contra restricciones dietéticas en UNA sola llamada al LLM.
    
    En lugar de hacer N llamadas (1 por receta), agrupa las recetas y pide al LLM
    que devuelva una lista de las que cumplen las restricciones.
    
    Args:
        llm: Instancia de ChatGroq
        recipes: Lista de objetos Recipe a validar
        restrictions_text: Texto con las restricciones (ej: "sin gluten, sin lactosa")
        diet_text: Texto con las dietas (ej: "vegan, vegetarian")
        batch_size: Número de recetas por batch (default 10)
    
    Returns:
        Lista de recetas que cumplen las restricciones
    """
    if not recipes:
        return []
    
    valid_recipes = []
    
    for i in range(0, len(recipes), batch_size):
        batch = recipes[i:i + batch_size]
        
        # Construir lista de recetas para el prompt
        recipes_list = "\n".join([
            f"{idx + 1}. {r.name} - Ingredientes: {r.ingredients[:200] if r.ingredients else 'N/A'}"
            for idx, r in enumerate(batch)
        ])
        
        diet_line = f"Dietas requeridas: [{diet_text}]." if diet_text else ""
        
        prompt = f"""Eres un experto en nutrición. Analiza estas recetas y determina cuáles cumplen con las restricciones del usuario.

Restricciones alimentarias: [{restrictions_text}]
{diet_line}

Recetas a evaluar:
{recipes_list}

INSTRUCCIONES:
- Responde SOLO con los NÚMEROS de las recetas que SÍ cumplen con las restricciones.
- Separa los números con comas.
- Si ninguna cumple, responde "NINGUNA".
- No incluyas explicaciones.

Ejemplo de respuesta válida: 1, 3, 5, 7
"""
        
        try:
            response = _invoke_with_retry(llm, prompt)
            answer = response.content.strip()
            
            logger.info(f"Batch {i//batch_size + 1}: LLM respondió: {answer}")
            
            # Parsear respuesta
            if answer.upper() != "NINGUNA":
                try:
                    valid_indices = [int(x.strip()) - 1 for x in answer.split(",") if x.strip().isdigit()]
                    for idx in valid_indices:
                        if 0 <= idx < len(batch):
                            valid_recipes.append(batch[idx])
                except ValueError:
                    logger.warning(f"No se pudo parsear respuesta: {answer}")
                    # En caso de error, incluir todas como fallback
                    valid_recipes.extend(batch)
        
        except RateLimitError as e:
            logger.warning(f"Rate limit alcanzado, esperando... {e}")
            time.sleep(60)  # Esperar 1 minuto completo
            # Reintentar este batch
            continue
        
        except Exception as e:
            logger.error(f"Error validando batch: {e}")
            # En caso de error, incluir todas como fallback
            valid_recipes.extend(batch)
    
    return valid_recipes


def validate_single_recipe(
    llm,
    recipe_name: str,
    ingredients: str,
    restrictions_text: str,
    diet_text: str = ""
) -> bool:
    """
    Valida una sola receta contra restricciones dietéticas.
    Incluye manejo de rate limits con retry automático.
    
    Args:
        llm: Instancia de ChatGroq
        recipe_name: Nombre de la receta
        ingredients: Lista de ingredientes
        restrictions_text: Restricciones del usuario
        diet_text: Dietas del usuario (opcional)
    
    Returns:
        True si la receta cumple las restricciones, False si no
    """
    diet_line = f"y requiero dietas: [{diet_text}]." if diet_text else ""
    
    message = (
        f"Responde SOLO con YES o NO. "
        f"Tengo un perfil dietético con restricciones: [{restrictions_text}] {diet_line}"
        f"¿Esta receta cumple con mis restricciones? {recipe_name} Ingredientes: [{ingredients}]"
    )
    
    try:
        response = _invoke_with_retry(llm, message)
        answer = response.content.strip().upper()
        return answer == "YES"
    
    except Exception as e:
        logger.error(f"Error validando receta {recipe_name}: {e}")
        return True  # En caso de error, incluir la receta


def _invoke_with_retry(llm, message: str, max_retries: int = MAX_RETRIES):
    """
    Invoca el LLM con retry automático para rate limits.
    Implementa exponential backoff.
    """
    for attempt in range(max_retries):
        try:
            return llm.invoke(message)
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = BASE_WAIT_TIME ** (attempt + 1)
                logger.warning(f"Rate limit, reintentando en {wait_time}s... (intento {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise
        
        except Exception as e:
            logger.error(f"Error en llamada al LLM: {e}")
            raise
    
    raise Exception("Max retries alcanzado")


def estimate_tokens(text: str) -> int:
    """
    Estima el número de tokens en un texto.
    Groq usa aproximadamente 4 caracteres por token.
    """
    return len(text) // 4
