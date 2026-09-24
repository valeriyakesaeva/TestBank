import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse
    ):
        deposit_account_request = DepositAccountRequest(
            accountId=created_account.id,
            amount=1000
        )
        deposit_account_response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)

        assert deposit_account_response.id == created_account.id
        assert deposit_account_response.balance == pytest.approx(created_account.balance + deposit_account_request.amount)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_response.id)
        assert account_from_db is not None, 'Аккаунт не создан, id аккаунта нет в БД'
        assert account_from_db.id == deposit_account_response.id, 'ID счёта в БД не совпадает с ID из ответа API'
        assert account_from_db.balance == pytest.approx(deposit_account_response.balance), 'Баланс счёта в БД не совпадает с балансом из ответа API'


    @pytest.mark.parametrize("amount", [999.99, 9000.01], ids=["below_minimum", "above_maximum"])
    def test_deposit_account_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, created_account: CreateAccountResponse, amount: float):
        deposit_account_request = DepositAccountRequest(
            accountId=created_account.id,
            amount=amount
        )
        error_response = api_manager.user_steps.deposit_account_invalid(create_user_request, deposit_account_request)

        assert error_response.json()['error'] == "Amount must be between 1000 and 9000"

        db_session.expire_all()

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db is not None, 'Счет удален'
        assert account_from_db.balance == pytest.approx(created_account.balance), 'Баланс изменился после отклонённого пополнения'
