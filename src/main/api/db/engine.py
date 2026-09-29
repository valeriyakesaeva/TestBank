from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config


# фабрика соединений с базой, создаёт объект для подключения к базе данных
engine = create_engine(Config.fetch('dataBaseUrl'), echo=False) # echo=False — отключает подробный показ SQL-запросов
# создаёт фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(bind=engine) # bind указывает, к какому объекту подключения должна быть привязана будущая сессия.
