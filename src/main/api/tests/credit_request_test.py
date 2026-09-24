import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account: CreateAccountResponse,
    ):
        credit_request = CreditRequest(
            accountId=credit_account.id,
            amount=5000,
            termMonths=12
        )
        credit_response = api_manager.user_steps.credit_request(credit_user_request, credit_request)

        assert credit_response.creditId > 0, 'Кредитный счет не создан'
        assert credit_response.id == credit_request.accountId
        assert credit_response.amount == pytest.approx(credit_request.amount)
        assert credit_response.termMonths == credit_request.termMonths
        assert credit_response.balance == pytest.approx(credit_request.amount)

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        account_from_db = Account.get_account_by_id(db_session, credit_account.id)

        assert credit_from_db is not None, 'Кредит не найден в БД'
        assert account_from_db is not None, 'Счёт не найден в БД'

        assert credit_from_db.id == credit_response.creditId
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == pytest.approx(credit_request.amount)
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == pytest.approx(-credit_request.amount)

        assert account_from_db.balance == pytest.approx(credit_account.balance + credit_request.amount)

    @pytest.mark.parametrize(
        'amount', [4999.99, 15000.01], ids=["below_minimum", "above_maximum"]
    )
    def test_credit_request_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request:CreateUserRequest,
            credit_account:CreateAccountResponse,
            amount: float,
    ):
        credit_request = CreditRequest(
            accountId=credit_account.id,
            amount=amount,
            termMonths=12
        )
        error_response = api_manager.user_steps.credit_request_invalid(credit_user_request, credit_request)

        assert error_response.json()['error'] == 'Amount must be between 5000 and 15000'

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_account.id)
        account_from_db = Account.get_account_by_id(db_session, credit_account.id)

        assert credit_from_db is None, 'Кредит был создан'
        assert account_from_db is not None, 'Счёт не найден в БД'
        assert account_from_db.balance == pytest.approx(credit_account.balance), 'Баланс счёта изменился после отклонённого запроса кредита'
