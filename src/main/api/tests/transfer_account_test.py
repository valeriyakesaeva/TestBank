import pytest
from sqlalchemy.orm import Session
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_accounts: tuple[DepositAccountResponse, CreateAccountResponse],
    ):
        from_account, to_account = funded_accounts
        transfer_request = TransferAccountRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=500
        )
        transfer_response = api_manager.user_steps.transfer_account(create_user_request, transfer_request)

        assert transfer_response.fromAccountId == from_account.id
        assert transfer_response.toAccountId == to_account.id
        assert transfer_response.fromAccountIdBalance == pytest.approx(from_account.balance - transfer_request.amount)

        db_session.expire_all()

        from_account_db = Account.get_account_by_id(
            db_session,
            from_account.id
        )

        to_account_db = Account.get_account_by_id(
            db_session,
            to_account.id
        )

        assert from_account_db is not None, 'Счет отправителя не найден'
        assert to_account_db is not None, 'Счет получателя не найден'
        assert from_account_db.balance == pytest.approx(transfer_response.fromAccountIdBalance)
        assert to_account_db.balance == pytest.approx(to_account.balance + transfer_request.amount)


    @pytest.mark.parametrize("amount", [499.99, 10000.01], ids=['below_minimum', 'above_maximum'])
    def test_transfer_account_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_accounts: tuple[DepositAccountResponse, CreateAccountResponse],
            amount: float,
    ):
        from_account, to_account = funded_accounts
        transfer_request = TransferAccountRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=amount
        )
        error_response = api_manager.user_steps.transfer_account_invalid(create_user_request, transfer_request)

        assert error_response.json()['error'] == "Amount must be between 500 and 10000"

        db_session.expire_all()

        from_account_db = Account.get_account_by_id(
            db_session,
            from_account.id
        )

        to_account_db = Account.get_account_by_id(
            db_session,
            to_account.id
        )

        assert from_account_db is not None, 'Счёт отправителя не найден'
        assert to_account_db is not None, 'Счёт получателя не найден'
        assert from_account_db.balance == pytest.approx(from_account.balance), 'Баланс отправителя изменен'
        assert to_account_db.balance == pytest.approx(to_account.balance), 'Баланс получателя изменен'







