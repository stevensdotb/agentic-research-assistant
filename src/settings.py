from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    OLLAMA_API_KEY: str = Field(default="<ollama_api_key>")
    MODEL_NAME: str = Field(default="llama3.2")

    # LangSmith for traceing
    LANGSMITH_TRACING: bool = Field(default=True)
    LANGSMITH_ENDPOINT: str = Field(default="https://api.smith.langchain.com")
    LANGSMITH_API_KEY: str = Field(default="<langsmith_api_key>")
    LANGCHAIN_PROJECT: str = Field(default="agentic-template")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()