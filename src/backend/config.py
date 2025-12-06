from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    whisper_model: str = "small"
    
    class Config:
        env_file = ".env"

settings = Settings()
