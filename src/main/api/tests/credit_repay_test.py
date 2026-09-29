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
            credit_repay_request: CreditRepayRequest
    ):
        credit_repay_response = api_manager.user_steps.credit_repay(credit_user_request,credit_repay_request)

        assert credit_repay_response.amountDeposited == pytest.approx(credit_repay_request.amount)

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            created_credit.creditId
        )
        account_from_db = Account.get_account_by_id(
            db_session,
            created_credit.id
        )

        assert credit_from_db.balance == pytest.approx(0), (
            f'Ожидалось полное погашение кредита, '
            f'фактический остаток долга {credit_from_db.balance}'
        )

        assert account_from_db.balance == pytest.approx(0), (
            f'Ожидался баланс счёта 0 после погашения, '
            f'фактический баланс {account_from_db.balance}'
        )

    def test_credit_repay_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            created_credit: CreditResponse,
            invalid_credit_repay_request: CreditRepayRequest
    ):
        error_response = api_manager.user_steps.credit_repay_invalid(credit_user_request, invalid_credit_repay_request)

        expected_credit_balance = -created_credit.amount

        credit_balance_text = (
            f'{expected_credit_balance:.2f}'
            .rstrip('0')
            .rstrip('.')
        )

        expected_error = (
            f'The amount is not enough. '
            f'Credit balance: {credit_balance_text}'
        )

        assert error_response.json()['error'] == expected_error

        db_session.expire_all()

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            created_credit.creditId
        )
        account_from_db = Account.get_account_by_id(
            db_session,
            created_credit.id
        )

        assert credit_from_db.balance == pytest.approx(
            expected_credit_balance
        ), (
            f'Ожидался неизменный долг '
            f'{expected_credit_balance}, фактический долг '
            f'{credit_from_db.balance}'
        )

        assert account_from_db.balance == pytest.approx(
            created_credit.amount
        ), (
            f'Ожидался неизменный баланс '
            f'{created_credit.amount}, фактический баланс '
            f'{account_from_db.balance}'
        )