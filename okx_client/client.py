"""
Основной клиент для работы с OKX API
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Импорт библиотеки OKX
from okx.Account import AccountAPI
from okx.MarketData import MarketAPI
from okx.PublicData import PublicAPI
from okx.Trade import TradeAPI

# Импорт собственных модулей
from okx_client.config import Config
from okx_client.models import Base
from okx_client.managers.public_data import PublicDataManager
from okx_client.managers.account import AccountManager
from okx_client.managers.trade import TradeManager

class OKXClient:
    """Основной клиент для работы с OKX API"""

    def __init__(self, api_key: str = None, secret_key: str = None,
                 passphrase: str = None, demo_mode: bool = None):
        """
        Инициализация клиента OKX

        Args:
            api_key: API ключ (если None, берется из конфига)
            secret_key: Секретный ключ (если None, берется из конфига)
            passphrase: Парольная фраза (если None, берется из конфига)
            demo_mode: Режим демо-торговли (если None, берется из конфига)
        """
        # Используем значения из аргументов или из конфига
        self.api_key = api_key or Config.API_KEY
        self.secret_key = secret_key or Config.API_SECRET
        self.passphrase = passphrase or Config.PASSPHRASE
        self.demo_mode = demo_mode if demo_mode is not None else Config.DEMO_MODE
        self.flag = "1" if self.demo_mode else "0"

        # Проверка ключей
        self._validate_keys()

        # Инициализация
        self._init_api_clients()
        self._init_database()
        self._init_managers()

        print("✅ OKXClient успешно инициализирован")

    def _validate_keys(self):
        """Проверка корректности ключей"""
        if not self.secret_key or not isinstance(self.secret_key, str):
            raise ValueError("Секретный ключ не может быть пустым и должен быть строкой")

        print("=" * 50)
        print("ИНИЦИАЛИЗАЦИЯ КЛИЕНТА")
        print("=" * 50)
        print(f"Режим: {'Демо (test)' if self.demo_mode else 'Реальный (live)'}")
        print(f"API Key: {self.api_key[:10]}..." if self.api_key else "API Key: НЕ УСТАНОВЛЕН")
        print(f"Secret Key: {self.secret_key[:10]}..." if self.secret_key else "Secret Key: НЕ УСТАНОВЛЕН")
        print(f"Passphrase: {'*' * len(self.passphrase)}" if self.passphrase else "Passphrase: НЕ УСТАНОВЛЕН")
        print("=" * 50)

    def _init_api_clients(self):
        """Инициализация API клиентов OKX"""
        try:
            # Для приватных запросов (баланс, ордера) нужны все ключи
            self.account_api = AccountAPI(self.api_key, self.secret_key,
                                        self.passphrase, False, self.flag)
            self.trade_api = TradeAPI(self.api_key, self.secret_key,
                                    self.passphrase, False, self.flag)

            # Для публичных запросов ключи не нужны
            self.public_api = PublicAPI(flag=self.flag)
            self.market_api = MarketAPI(flag=self.flag)

            print("✅ API клиенты инициализированы")

        except Exception as e:
            print(f"❌ Ошибка инициализации API клиентов: {e}")
            raise

    def _init_database(self):
        """Инициализация базы данных SQLite"""
        try:
            engine = create_engine(Config.DATABASE_URL, echo=False)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            self.db_session = Session()
            print("✅ База данных SQLite инициализирована")
        except Exception as e:
            print(f"❌ Ошибка инициализации базы данных: {e}")
            raise

    def _init_managers(self):
        """Инициализация менеджеров"""
        self.public = PublicDataManager(self.public_api, self.market_api)
        self.account = AccountManager(self.account_api)
        self.trader = TradeManager(self.trade_api, self.db_session)
        print("✅ Менеджеры инициализированы")

    def close(self):
        """Закрытие соединения с БД"""
        self.db_session.close()
        print("✅ Соединение с БД закрыто")

    def __enter__(self):
        """Поддержка контекстного менеджера (with statement)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие соединения при выходе из контекста"""
        self.close()

    def test_connection(self):
        pass
