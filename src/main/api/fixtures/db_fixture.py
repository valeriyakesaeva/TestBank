import pytest
from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope="function")
def db_session():
    #Конкретная рабочая сессия одного теста
    connection = engine.connect()
    transaction = connection.begin() # .begin() - создает транзакцию
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback() # Если внутри блока произошла ошибка → автоматически выполняется rollback()
        connection.close()