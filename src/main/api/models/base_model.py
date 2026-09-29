from pydantic import BaseModel as BM

class BaseModel(BM):
    pass

#Общая базовая модель Pydantic. Собственный BaseModel пока ничего не добавляет. Он создаёт одну точку
# для будущих общих настроек всех моделей.