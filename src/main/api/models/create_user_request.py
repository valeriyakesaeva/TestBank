from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

#Модель запроса создания пользователя
class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r'^[A-Za-z0-9]{3,15}$')] #3-15 английских букв или цифр
    password: Annotated[str, CreationRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')] #3 заглавные + 1 строчная + 2
    # цифры + 4 специальных символа
    role: Annotated[str, CreationRule(regex=r'^ROLE_USER$')] #строго ROLE_USER
