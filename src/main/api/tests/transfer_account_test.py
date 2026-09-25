import pytest
from sqlalchemy.orm import Session
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.test_data.bank_rules import BankRules


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_accounts: tuple[DepositAccountResponse, CreateAccountResponse],
            transfer_request: TransferAccountRequest,
    ):
        from_account, to_account = funded_accounts
        transfer_response = api_manager.user_steps.transfer_account(create_user_request, transfer_request)
        expected_from_balance = (from_account.balance - transfer_request.amount)
        expected_to_balance = (to_account.balance + transfer_request.amount)

        assert transfer_response.fromAccountIdBalance == pytest.approx(expected_from_balance)

        db_session.expire_all()

        from_account_db = Account.get_account_by_id(db_session, from_account.id)

        to_account_db = Account.get_account_by_id(db_session, to_account.id)

        assert from_account_db.balance == pytest.approx(expected_from_balance), (
            f'Ожидался баланс отправителя {expected_from_balance}, '
            f'фактический баланс {from_account_db.balance}'
        )

        assert to_account_db.balance == pytest.approx(expected_to_balance), (
            f'Ожидался баланс получателя {expected_to_balance}, '
            f'фактический баланс {to_account_db.balance}'
        )


    @pytest.mark.parametrize(
        'invalid_transfer_request',
        [
            BankRules.TRANSFER_MIN_AMOUNT - 0.01,
            BankRules.TRANSFER_MAX_AMOUNT + 0.01
        ],
        ids=['below_minimum', 'above_maximum'],
        indirect=True
    )
    def test_transfer_account_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_accounts: tuple[DepositAccountResponse, CreateAccountResponse],
            invalid_transfer_request: TransferAccountRequest,
    ):
        from_account, to_account = funded_accounts
        error_response = api_manager.user_steps.transfer_account_invalid(create_user_request, invalid_transfer_request)

        expected_error = (
            f'Amount must be between '
            f'{BankRules.TRANSFER_MIN_AMOUNT:g} and '
            f'{BankRules.TRANSFER_MAX_AMOUNT:g}'
        )

        assert error_response.json()['error'] == expected_error

        db_session.expire_all()

        from_account_db = Account.get_account_by_id(
            db_session,
            from_account.id
        )

        to_account_db = Account.get_account_by_id(
            db_session,
            to_account.id
        )

        assert from_account_db.balance == pytest.approx(
            from_account.balance
        ), (
            f'Ожидался неизменный баланс отправителя '
            f'{from_account.balance}, фактический баланс '
            f'{from_account_db.balance}'
        )

        assert to_account_db.balance == pytest.approx(
            to_account.balance
        ), (
            f'Ожидался неизменный баланс получателя '
            f'{to_account.balance}, фактический баланс '
            f'{to_account_db.balance}'
        )







