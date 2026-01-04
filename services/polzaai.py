"""PolzaAI API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional, AsyncIterator, Tuple
from .config import POLZAAI_API_KEY, POLZAAI_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via PolzaAI API.

    Args:
        model: PolzaAI model identifier (e.g., "openai/gpt-4o")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    print(f"Using API Key: {POLZAAI_API_KEY[:10] if POLZAAI_API_KEY else 'None'}...")
    headers = {
        "Authorization": f"Bearer {POLZAAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                POLZAAI_API_URL,
                headers=headers,
                json=payload
            )
            
            # Check if status code indicates success (200 or 201)
            if response.status_code not in [200, 201]:
                print(f"Error querying model {model}: Status {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
            # Try to parse JSON response
            try:
                data = response.json()
            except Exception as json_error:
                print(f"Error parsing JSON response for model {model}: {json_error}")
                print(f"Raw response: {response.text}")
                return None
            
            # Check if the expected structure exists in the response
            if 'choices' not in data or not data['choices']:
                print(f"No choices in response for model {model}")
                print(f"Response: {data}")
                return None
                
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of PolzaAI model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    print(f"Querying models: {models}")
    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]
    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}


async def query_models_stream(
    models: List[str],
    messages: List[Dict[str, str]]
) -> AsyncIterator[Tuple[str, Optional[Dict[str, Any]]]]:
    """
    Stream model responses as they become available.
    
    Args:
        models: List of PolzaAI model identifiers
        messages: List of message dicts to send to each model
    
    Yields:
        Tuple of (model_name, response) as responses become available
    """
    import asyncio
    from typing import AsyncIterator, Tuple, Optional, Dict, Any, List

    print(f"Querying models: {models}")

    # Create tasks for all models and keep track of which model each task corresponds to
    model_tasks = [(model, asyncio.create_task(query_model(model, messages))) for model in models]

    # Process results as they complete
    for model_name, task in model_tasks:
        try:
            response = await task
            yield model_name, response
        except Exception as e:
            print(f"Error querying model {model_name}: {e}")
            yield model_name, None
