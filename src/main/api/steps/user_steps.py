import allure
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requster import CrudRequester
from requests import Response
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        with allure.step('Создание счета'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post()
            return response

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        with allure.step('Пополнение банковского счета'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.DEPOSIT_ACCOUNT,
                ResponseSpecs.request_ok()
            ).post(deposit_account_request)
            return response

    def deposit_account_invalid(
            self,
            create_user_request: CreateUserRequest,
            deposit_account_request: DepositAccountRequest
    ) -> Response:
        with allure.step('Неуспешное пополнение банковского счёта'):
            response = CrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.DEPOSIT_ACCOUNT,
                ResponseSpecs.request_bad()
            ).post(deposit_account_request)
            return response

    def transfer_account(
            self,
            create_user_request: CreateUserRequest,
            transfer_account_request: TransferAccountRequest
    ) -> TransferAccountResponse:
        with allure.step('Перевод денежных средств между счетами'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER_ACCOUNT,
                ResponseSpecs.request_ok()
            ).post(transfer_account_request)
            return response

    def transfer_account_invalid(
            self,
            create_user_request: CreateUserRequest,
            transfer_account_request: TransferAccountRequest
    ) -> Response:
        with allure.step('Неуспешный перевод денежных средств между счетами'):
            response = CrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password),
                Endpoint.TRANSFER_ACCOUNT,
                ResponseSpecs.request_bad()
            ).post(transfer_account_request)
            return response

    def credit_request(
            self,
            credit_user_request: CreateUserRequest,
            credit_request: CreditRequest
    ) -> CreditResponse:
        with allure.step('Запрос кредита'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_created()
            ).post(credit_request)
            return response

    def credit_request_invalid(
            self,
            credit_user_request: CreateUserRequest,
            credit_request: CreditRequest
    ) -> Response:
        with allure.step('Неуспешный запрос кредита'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_bad()
            ).post(credit_request)
            return response

    def credit_repay(
            self,
            credit_user_request: CreateUserRequest,
            credit_repay_request: CreditRepayRequest
    ) -> CreditRepayResponse:
        with allure.step('Полное погашение кредита'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_ok()
            ).post(credit_repay_request)
            return response

    def credit_repay_invalid(
            self,
            credit_user_request: CreateUserRequest,
            credit_repay_request: CreditRepayRequest
    ) -> Response:
        with allure.step('Неуспешное погашение кредита'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_unprocessable_entity()
            ).post(credit_repay_request)
            return response
