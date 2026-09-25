import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.test_data.bank_rules import BankRules


@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse,
            deposit_request: DepositAccountRequest
    ):
        deposit_account_response = api_manager.user_steps.deposit_account(create_user_request, deposit_request)
        expected_balance = (created_account.balance + deposit_request.amount)

        assert deposit_account_response.balance == pytest.approx(expected_balance)

        db_session.expire_all()

        account_from_db = Account.get_account_by_id(db_session, deposit_account_response.id)
        assert account_from_db is not None, f'Ожидалось наличие счёта {created_account.id} в БД'
        assert account_from_db.balance == pytest.approx(expected_balance), (
            f'Ожидался баланс {expected_balance}, '
            f'фактический баланс {account_from_db.balance}'
        )


    @pytest.mark.parametrize(
        'invalid_deposit_request',
        [
            BankRules.DEPOSIT_MIN_AMOUNT - 0.01,
            BankRules.DEPOSIT_MAX_AMOUNT + 0.01,
        ],
        ids=["below_minimum", "above_maximum"],
        indirect=True
    )
    def test_deposit_account_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse,
            invalid_deposit_request: DepositAccountRequest
    ):
        error_response = api_manager.user_steps.deposit_account_invalid(create_user_request, invalid_deposit_request)

        expected_error = (
            f'Amount must be between '
            f'{BankRules.DEPOSIT_MIN_AMOUNT:g} and '
            f'{BankRules.DEPOSIT_MAX_AMOUNT:g}'
        )

        assert error_response.json()['error'] == expected_error

        db_session.expire_all()

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db is not None, f'Ожидалось наличие счёта {created_account.id} в БД'
        assert account_from_db.balance == pytest.approx(created_account.balance), (
            f'Ожидался неизменный баланс {created_account.balance}, '
            f'фактический баланс {account_from_db.balance}'
        )