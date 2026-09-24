import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            created_credit: CreditResponse,
    ):
        credit_repay_request = CreditRepayRequest(
            creditId=created_credit.creditId,
            accountId=created_credit.id,
            amount=created_credit.amount
        )
        credit_repay_response = api_manager.user_steps.credit_repay(credit_user_request, credit_repay_request)

        assert credit_repay_response.creditId == created_credit.creditId
        assert credit_repay_response.amountDeposited == pytest.approx(
            credit_repay_request.amount
        )

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(db_session, created_credit.creditId)
        account_from_db = Account.get_account_by_id(db_session, created_credit.id)

        assert credit_from_db is not None, 'Кредит не найден в БД'
        assert account_from_db is not None, 'Счёт не найден в БД'

        assert credit_from_db.balance == pytest.approx(0)
        assert account_from_db.balance == pytest.approx(created_credit.amount - credit_repay_request.amount)


    def test_credit_repay_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            created_credit: CreditResponse,
    ):
        credit_repay_request = CreditRepayRequest(
            creditId=created_credit.creditId,
            accountId=created_credit.id,
            amount=created_credit.amount - 0.01
        )
        error_response = api_manager.user_steps.credit_repay_invalid(credit_user_request, credit_repay_request)

        assert error_response.json()['error'] == ('The amount is not enough. Credit balance: -5000')

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(db_session, created_credit.creditId)
        account_from_db = Account.get_account_by_id(db_session, created_credit.id)

        assert credit_from_db is not None, 'Кредит не найден в БД'
        assert account_from_db is not None, 'Счёт не найден в БД'

        assert credit_from_db.balance == pytest.approx(-created_credit.amount)
        assert account_from_db.balance == pytest.approx(created_credit.amount)

