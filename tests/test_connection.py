import httpx
import pytest
from src.settings import settings


@pytest.mark.asyncio
async def test_ollama_connection():
    """Test the model connection to Ollama and its response."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            assert response.status_code == 200
            models = response.json().get("models", [])
            
            model_names = [model['name'] for model in models]
            assert any(settings.MODEL_NAME in name for name in model_names)
            print(f"\n✅ Connected. Detected models: {len(models)}")
    except Exception as e:
        pytest.fail(f"Connection to Ollama failed at {settings.OLLAMA_BASE_URL}. Is it up and running? Error: {e}")
