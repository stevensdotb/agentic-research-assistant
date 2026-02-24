from src.settings import settings

def test_settings_load():
    assert settings.OLLAMA_BASE_URL is not None
    assert isinstance(settings.MODEL_NAME, str)
    print(f"\n✅ Config loaded: {settings.MODEL_NAME}")