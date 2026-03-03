"""
Gestión eficiente de memoria y contexto para el agente nutricional.
Optimizado para entornos con GPU limitada (8GB VRAM).

Configuración actual:
- OLLAMA_CONTEXT_LENGTH: 32768 (docker-compose)
- num_ctx: 16384 (config_ollama)
- MAX_CONTEXT_TOKENS: 10000 (memory.py)
"""
from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.messages.utils import count_tokens_approximately
import logging
import copy

logger = logging.getLogger(__name__)

# Configuración de límites - valores aumentados para preservar contexto del plan
MAX_CONTEXT_TOKENS = 10000  # Aumentado de 4000 para no perder contexto
TOOL_RESULT_MAX_LENGTH = 6000  # Aumentado de 2000 para planes completos

class ConversationMemory:
    """
    Gestiona el historial de conversación de forma eficiente.
    Implementa estrategias de compresión conservadoras.
    """
    
    @staticmethod
    def count_tokens(messages: List[BaseMessage]) -> int:
        """Cuenta tokens aproximados en una lista de mensajes."""
        if not messages:
            return 0
        return count_tokens_approximately(messages)
    
    @staticmethod
    def compress_tool_results(messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Comprime resultados de herramientas que sean muy largos.
        CONSERVADOR: Solo comprime si excede TOOL_RESULT_MAX_LENGTH.
        Mantiene la estructura original del mensaje.
        """
        if not messages:
            return []
        
        # Crear copia para no modificar originales
        compressed = []
        
        for msg in messages:
            # Solo procesar ToolMessages
            if hasattr(msg, 'type') and msg.type == 'tool':
                content = getattr(msg, 'content', '')
                
                # Si el contenido es un dict, extraer 'result' si existe
                if isinstance(content, dict):
                    result_text = content.get('result', str(content))
                    if len(result_text) > TOOL_RESULT_MAX_LENGTH:
                        # Comprimir manteniendo inicio y final
                        truncated = result_text[:TOOL_RESULT_MAX_LENGTH - 100] + "\n\n[...contenido truncado...]\n\n" + result_text[-100:]
                        # Crear copia del mensaje con contenido comprimido
                        new_content = content.copy()
                        new_content['result'] = truncated
                        msg = _copy_message_with_content(msg, new_content)
                        logger.debug(f"🗜️ Tool result comprimido: {len(result_text)} -> {len(truncated)} chars")
                
                elif isinstance(content, str) and len(content) > TOOL_RESULT_MAX_LENGTH:
                    truncated = content[:TOOL_RESULT_MAX_LENGTH - 100] + "\n\n[...contenido truncado...]\n\n" + content[-100:]
                    msg = _copy_message_with_content(msg, truncated)
                    logger.debug(f"🗜️ Tool result comprimido: {len(content)} -> {len(truncated)} chars")
            
            compressed.append(msg)
        
        return compressed
    
    @staticmethod
    def extract_essential_context(messages: List[BaseMessage], max_tokens: int = MAX_CONTEXT_TOKENS) -> List[BaseMessage]:
        """
        Extrae el contexto esencial manteniendo los mensajes más recientes.
        Estrategia conservadora: prioriza mensajes recientes.
        """
        if not messages:
            return []
        
        # Siempre mantener los últimos 6 mensajes (3 turnos de conversación)
        min_messages = min(6, len(messages))
        essential = messages[-min_messages:]
        
        current_tokens = ConversationMemory.count_tokens(essential)
        
        # Si tenemos espacio y más mensajes, añadir anteriores
        if current_tokens < max_tokens and len(messages) > min_messages:
            remaining_tokens = max_tokens - current_tokens
            
            for msg in reversed(messages[:-min_messages]):
                msg_tokens = count_tokens_approximately([msg])
                if msg_tokens <= remaining_tokens:
                    essential.insert(0, msg)
                    remaining_tokens -= msg_tokens
                else:
                    break
        
        return essential


def _copy_message_with_content(msg: BaseMessage, new_content: Any) -> BaseMessage:
    """
    Crea una copia del mensaje con nuevo contenido.
    Preserva todos los atributos originales.
    """
    try:
        # Intentar crear copia usando el constructor
        msg_dict = {
            'content': new_content,
            'name': getattr(msg, 'name', None),
            'tool_call_id': getattr(msg, 'tool_call_id', None),
        }
        # Filtrar None values
        msg_dict = {k: v for k, v in msg_dict.items() if v is not None}
        
        # Usar el mismo tipo de mensaje
        msg_type = type(msg)
        return msg_type(**msg_dict)
    except Exception:
        # Fallback: modificar in-place (menos ideal pero funciona)
        msg.content = new_content
        return msg


def optimize_state_for_inference(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimiza el estado completo antes de enviarlo al modelo.
    
    IMPORTANTE: Esta función es CONSERVADORA para no romper el flujo del agente.
    Solo aplica compresión cuando es necesario.
    
    Args:
        state: Estado del grafo con messages, profile, etc.
    
    Returns:
        Estado optimizado (copia, no modifica el original)
    """
    # Crear copia superficial del estado
    optimized = state.copy()
    
    if 'messages' not in optimized or not optimized['messages']:
        return optimized
    
    messages = optimized['messages']
    original_count = len(messages)
    original_tokens = ConversationMemory.count_tokens(messages)
    
    # Solo optimizar si excedemos el límite
    if original_tokens > MAX_CONTEXT_TOKENS:
        logger.info(f"📊 Optimizando: {original_tokens} tokens > {MAX_CONTEXT_TOKENS} límite")
        
        # 1. Comprimir tool results largos
        messages = ConversationMemory.compress_tool_results(messages)
        
        # 2. Si aún excede, extraer contexto esencial
        current_tokens = ConversationMemory.count_tokens(messages)
        if current_tokens > MAX_CONTEXT_TOKENS:
            messages = ConversationMemory.extract_essential_context(messages, MAX_CONTEXT_TOKENS)
        
        optimized['messages'] = messages
        
        final_tokens = ConversationMemory.count_tokens(messages)
        logger.info(f"✅ Optimizado: {original_count} -> {len(messages)} mensajes, {original_tokens} -> {final_tokens} tokens")
    else:
        logger.debug(f"📊 Sin optimización necesaria: {original_tokens} tokens")
    
    return optimized


# Utilidades adicionales para diagnóstico
def get_state_stats(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Devuelve estadísticas del estado para diagnóstico.
    """
    messages = state.get('messages', [])
    
    stats = {
        'total_messages': len(messages),
        'total_tokens': ConversationMemory.count_tokens(messages),
        'message_types': {},
        'tool_calls': [],
    }
    
    for msg in messages:
        msg_type = type(msg).__name__
        stats['message_types'][msg_type] = stats['message_types'].get(msg_type, 0) + 1
        
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                stats['tool_calls'].append(tc.get('name', 'unknown'))
    
    return stats
