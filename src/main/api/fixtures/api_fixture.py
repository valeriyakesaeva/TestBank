from src.main.api.classes.api_manager import ApiManager
import pytest

@pytest.fixture
def api_manager(created_obj):
    return ApiManager(created_obj)
#Pytest сам сначала создаёт created_obj, потому что это аргумент фикстуры api_manager.