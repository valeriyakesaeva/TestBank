from http import HTTPStatus
from requests import Response

class ResponseSpecs:
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created():
#`request_created()` возвращает функцию `confirm`. Позже requester передаёт в неё настоящий Response.
# Такой приём называется функцией высшего порядка.
#Совсем просто. Сначала мы заказываем правило «ожидаю 201», а после ответа правило получает response и проверяет его.
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def request_unprocessable_entity():
        def confirm(response: Response):
            assert (response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY), response.text
        return confirm