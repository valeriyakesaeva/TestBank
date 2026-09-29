from src.main.api.models.base_model import BaseModel

class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str
 #model_validate(response.json())` проверяет наличие полей и их типы, затем создаёт удобный Python-объект.