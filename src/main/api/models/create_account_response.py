from src.main.api.models.base_model import BaseModel

class CreateAccountResponse(BaseModel):
    id: int
    number: str
    balance: float

    #model_validate(response.json())` проверяет наличие полей и их типы, затем создаёт удобный Python-объект.