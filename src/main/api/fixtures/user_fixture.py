import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest

#фикстура не только создаёт request-модель, но и уже отправляет её на сервер, создавая пользователя
@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def credit_user_request(api_manager) -> CreateUserRequest:
    generated_user = RandomModelGenerator.generate(CreateUserRequest)

    credit_user = generated_user.model_copy(
        update={'role': 'ROLE_CREDIT_SECRET'})
    api_manager.admin_steps.create_user(credit_user)

    return credit_user



