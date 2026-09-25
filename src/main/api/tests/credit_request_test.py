import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequest
from src.main.api.test_data.bank_rules import BankRules


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account: CreateAccountResponse,
            credit_request: CreditRequest
    ):
        credit_response = api_manager.user_steps.credit_request(credit_user_request, credit_request)
        expected_api_balance = credit_request.amount
        expected_credit_balance = -credit_request.amount
        expected_account_balance = (credit_account.balance + credit_request.amount)

        assert credit_response.balance == pytest.approx(expected_api_balance)

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        account_from_db = Account.get_account_by_id(db_session, credit_account.id)

        assert credit_from_db.balance == pytest.approx(
            expected_credit_balance
        ), (
            f'Ожидался долг {expected_credit_balance}, '
            f'фактический долг {credit_from_db.balance}'
        )

        assert account_from_db.balance == pytest.approx(
            expected_account_balance
        ), (
            f'Ожидался баланс счёта {expected_account_balance}, '
            f'фактический баланс {account_from_db.balance}'
        )

    @pytest.mark.parametrize(
        'invalid_credit_request',
        [
            BankRules.CREDIT_MIN_AMOUNT - 0.01,
            BankRules.CREDIT_MAX_AMOUNT + 0.01
        ],
        ids=['below_minimum', 'above_maximum'],
        indirect=True
    )
    def test_credit_request_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request:CreateUserRequest,
            credit_account:CreateAccountResponse,
            invalid_credit_request: CreditRequest,
    ):
        error_response = api_manager.user_steps.credit_request_invalid(credit_user_request, invalid_credit_request)
        expected_error = (
            f'Amount must be between '
            f'{BankRules.CREDIT_MIN_AMOUNT:g} and '
            f'{BankRules.CREDIT_MAX_AMOUNT:g}'
        )

        assert error_response.json()['error'] == expected_error

        db_session.expire_all()

        account_from_db = Account.get_account_by_id(db_session, credit_account.id)

        assert account_from_db.balance == pytest.approx(
            credit_account.balance
        ), (
            f'Ожидался неизменный баланс '
            f'{credit_account.balance}, фактический баланс '
            f'{account_from_db.balance}'
        )