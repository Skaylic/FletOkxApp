# okx_client/config.py
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Загружаем переменные окружения
load_dotenv()


@dataclass
class Config:
    """Конфигурация приложения"""
    API_KEY: str = os.getenv("OKX_API_KEY", "")
    API_SECRET: str = os.getenv("OKX_API_SECRET", "")
    PASSPHRASE: str = os.getenv("OKX_PASSPHRASE", "")
    DEMO_MODE: bool = os.getenv("OKX_DEMO_MODE", "true").lower() == "true"

    # Настройки БД
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///okx_trades.db")

    # Настройки приложения
    REFRESH_INTERVAL: int = int(os.getenv("REFRESH_INTERVAL", "10"))
    MAX_TICKERS: int = int(os.getenv("MAX_TICKERS", "50"))
    MAX_ORDERS: int = int(os.getenv("MAX_ORDERS", "100"))

    # Настройки API
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_RETRY_COUNT: int = int(os.getenv("API_RETRY_COUNT", "3"))

    @classmethod
    def validate(cls):
        """Проверка конфигурации"""
        errors = []

        if not cls.API_KEY:
            errors.append("API_KEY не установлен")
        if not cls.API_SECRET:
            errors.append("API_SECRET не установлен")
        if not cls.PASSPHRASE:
            errors.append("PASSPHRASE не установлен")

        if errors:
            raise ValueError("Ошибки конфигурации: " + ", ".join(errors))

        return True
