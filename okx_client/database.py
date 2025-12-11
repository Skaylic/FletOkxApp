from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from okx_client.models import Base
from okx_client.config import Config


class DatabaseManager:
    def __init__(self, database_url=None):
        self.database_url = database_url or Config.DATABASE_URL
        self.engine = create_engine(self.database_url, echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()
