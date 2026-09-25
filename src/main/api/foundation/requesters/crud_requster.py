import json
from typing import Any, Optional

import allure
import requests
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else None
        safe_request_body = self._mask_sensitive_data(body)
        with allure.step(
            f"POST {Config.fetch('backendUrl')}"
            f"{self.endpoint.value.url}"
        ):
            allure.attach(
                json.dumps(
                    safe_request_body, ensure_ascii=False, indent=2), 'Request body', allure.attachment_type.JSON)
            response = requests.post(url=f'{Config.fetch("backendUrl")}{self.endpoint.value.url}',
                                     headers=self.request_spec,
                                     json=body
                                     )
            try:
                response_body = response.json()
            except ValueError:
                response_body = response.text

            safe_response_body = self._mask_sensitive_data(response_body)
            if isinstance(safe_response_body, (dict, list)):
                allure_response = json.dumps(safe_response_body, ensure_ascii=False, indent=2)
                attachment_type = allure.attachment_type.JSON
            else:
                allure_response = str(safe_response_body)
                attachment_type = allure.attachment_type.TEXT

            allure.attach(allure_response, 'Response body', attachment_type)

            allure.attach(str(response.status_code), 'Status code', allure.attachment_type.TEXT)

            self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f'{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    @staticmethod
    def _mask_sensitive_data(data: Any) -> Any:
        sensitive_fields = {
            'password',
            'token',
            'access_token',
            'authorization'
        }
        if isinstance(data, dict):
            return {
                key: (
                    '***'
                    if key.lower() in sensitive_fields
                    else CrudRequester._mask_sensitive_data(value)
                )
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [
                CrudRequester._mask_sensitive_data(item)
                for item in data
            ]
        return data


