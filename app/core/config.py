from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartLabKit AI Service"
    API_V1_STR: str = "/api/v1"

    MODEL_PATH: str = "weights/smartlab_yolo11n_v1.pt"
    DEFAULT_CONFIDENCE: float = 0.5

    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()