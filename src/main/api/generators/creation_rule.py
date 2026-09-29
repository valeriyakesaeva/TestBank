from attr import dataclass


@dataclass
class CreationRule:
    regex: str
#Это маленький контейнер, который хранит регулярное выражение. Сам он ничего не генерирует
    #CreationRule — это метаданные для вашего генератора, а не Pydantic-ограничение.
    # Поэтому Pydantic не отклонит username из русских букв. Это полезно для негативных API-
    # тестов, но это нужно понимать