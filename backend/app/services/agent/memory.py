"""
Efficient memory and context management for the nutritional agent.
Optimized for environments with limited GPU (8GB VRAM).

Current configuration:
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

# Configuration limits – increased to preserve plan context
MAX_CONTEXT_TOKENS = 10000  # Increased from 4000 to avoid losing context
TOOL_RESULT_MAX_LENGTH = 6000  # Increased from 2000 for full plans

class ConversationMemory:
    """
    Manages conversation history efficiently.
    Implements conservative compression strategies.
    """
    
    @staticmethod
    def count_tokens(messages: List[BaseMessage]) -> int:
        """Approximately counts tokens in a list of messages."""
        if not messages:
            return 0
        return count_tokens_approximately(messages)
    
    @staticmethod
    def compress_tool_results(messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Compresses tool results that are too long.
        CONSERVATIVE: Only compresses if it exceeds TOOL_RESULT_MAX_LENGTH.
        Preserves the original message structure.
        """
        if not messages:
            return []
        
        # Create a copy to avoid modifying originals
        compressed = []
        
        for msg in messages:
            # Only process ToolMessages
            if hasattr(msg, 'type') and msg.type == 'tool':
                content = getattr(msg, 'content', '')
                
                # If content is a dict, extract 'result' if it exists
                if isinstance(content, dict):
                    result_text = content.get('result', str(content))
                    if len(result_text) > TOOL_RESULT_MAX_LENGTH:
                        # Compress keeping beginning and end
                        truncated = result_text[:TOOL_RESULT_MAX_LENGTH - 100] + "\n\n[...truncated content...]\n\n" + result_text[-100:]
                        # Create a copy of the message with compressed content
                        new_content = content.copy()
                        new_content['result'] = truncated
                        msg = _copy_message_with_content(msg, new_content)
                        logger.debug(f"🗜️ Tool result compressed: {len(result_text)} -> {len(truncated)} chars")
                
                elif isinstance(content, str) and len(content) > TOOL_RESULT_MAX_LENGTH:
                    truncated = content[:TOOL_RESULT_MAX_LENGTH - 100] + "\n\n[...truncated content...]\n\n" + content[-100:]
                    msg = _copy_message_with_content(msg, truncated)
                    logger.debug(f"🗜️ Tool result compressed: {len(content)} -> {len(truncated)} chars")
            
            compressed.append(msg)
        
        return compressed
    
    @staticmethod
    def extract_essential_context(messages: List[BaseMessage], max_tokens: int = MAX_CONTEXT_TOKENS) -> List[BaseMessage]:
        """
        Extracts essential context keeping the most recent messages.
        Conservative strategy: prioritizes recent messages.
        """
        if not messages:
            return []
        
        # Always keep the last 6 messages (3 conversation turns)
        min_messages = min(6, len(messages))
        essential = messages[-min_messages:]
        
        current_tokens = ConversationMemory.count_tokens(essential)
        
        # If we have space and more messages, add older ones
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
    Creates a copy of the message with new content.
    Preserves all original attributes.
    """
    try:
        # Try to create a copy using the constructor
        msg_dict = {
            'content': new_content,
            'name': getattr(msg, 'name', None),
            'tool_call_id': getattr(msg, 'tool_call_id', None),
        }
        # Filter out None values
        msg_dict = {k: v for k, v in msg_dict.items() if v is not None}
        
        # Use the same message type
        msg_type = type(msg)
        return msg_type(**msg_dict)
    except Exception:
        # Fallback: modify in-place (less ideal but works)
        msg.content = new_content
        return msg


def optimize_state_for_inference(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimizes the entire state before sending it to the model.
    
    IMPORTANT: This function is CONSERVATIVE to avoid breaking the agent flow.
    Only applies compression when necessary.
    
    Args:
        state: Graph state with messages, profile, etc.
    
    Returns:
        Optimized state (copy, does not modify the original)
    """
    # Create shallow copy of the state
    optimized = state.copy()
    
    if 'messages' not in optimized or not optimized['messages']:
        return optimized
    
    messages = optimized['messages']
    original_count = len(messages)
    original_tokens = ConversationMemory.count_tokens(messages)
    
    # Only optimize if we exceed the limit
    if original_tokens > MAX_CONTEXT_TOKENS:
        logger.info(f"📊 Optimizing: {original_tokens} tokens > {MAX_CONTEXT_TOKENS} limit")
        
        # 1. Compress long tool results
        messages = ConversationMemory.compress_tool_results(messages)
        
        # 2. If still exceeding, extract essential context
        current_tokens = ConversationMemory.count_tokens(messages)
        if current_tokens > MAX_CONTEXT_TOKENS:
            messages = ConversationMemory.extract_essential_context(messages, MAX_CONTEXT_TOKENS)
        
        optimized['messages'] = messages
        
        final_tokens = ConversationMemory.count_tokens(messages)
        logger.info(f"✅ Optimized: {original_count} -> {len(messages)} messages, {original_tokens} -> {final_tokens} tokens")
    else:
        logger.debug(f"📊 No optimization needed: {original_tokens} tokens")
    
    return optimized


# Additional utilities for diagnostics
def get_state_stats(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns state statistics for diagnostics.
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