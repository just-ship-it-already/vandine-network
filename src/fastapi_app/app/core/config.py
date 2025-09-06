from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Vandine Network Monitor FastAPI"
    DEBUG: bool = False
    
    # Database
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000"]
    
    # Network Devices
    PI0_HOST: str = "192.168.1.100"
    PI0_USERNAME: str = "pi"
    PI0_PASSWORD: str = ""
    
    PI1_HOST: str = "192.168.1.101"
    PI1_USERNAME: str = "pi"
    PI1_PASSWORD: str = ""
    
    ROUTER_HOST: str = "192.168.1.1"
    ROUTER_USERNAME: str = "admin"
    ROUTER_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()