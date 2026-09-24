import pytest
from src.main.api.db.engine import SessionLocal
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from collections.abc import Callable, Generator

from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.db.crud.credit_crud import CreditCrudDb


@pytest.fixture
def account_factory(
        api_manager: ApiManager
) -> Generator[
    Callable[[CreateUserRequest], CreateAccountResponse],
    None,
    None
]:
    created_accounts: list[CreateAccountResponse] = []

    def create_account(user: CreateUserRequest) -> CreateAccountResponse:
        account_response = api_manager.user_steps.create_account(user)
        created_accounts.append(account_response)
        return account_response

    try:
        yield create_account
    finally:
        clean_session = SessionLocal()
        try:
            for account_response in created_accounts:
                TransactionCrudDb.delete_transactions_by_account_id(clean_session, account_response.id)
            for account_response in created_accounts:
                CreditCrudDb.delete_credits_by_account_id(clean_session, account_response.id)
            for account_response in reversed(created_accounts):
                AccountCrudDb.delete_account(clean_session, account_response.id)
        except Exception:
            clean_session.rollback()
            raise
        finally:
            clean_session.close()

@pytest.fixture
def created_account(
        account_factory: Callable[[CreateUserRequest],CreateAccountResponse],
        create_user_request: CreateUserRequest ) -> CreateAccountResponse:
    return account_factory(create_user_request)

@pytest.fixture
def created_accounts(
        account_factory: Callable[[CreateUserRequest],CreateAccountResponse],
        create_user_request: CreateUserRequest
) -> tuple[CreateAccountResponse, CreateAccountResponse]:
    first_account = account_factory(create_user_request)
    second_account = account_factory(create_user_request)

    return first_account, second_account

@pytest.fixture
def funded_accounts(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        created_accounts: tuple[CreateAccountResponse, CreateAccountResponse]
) -> tuple[DepositAccountResponse, CreateAccountResponse]:
    first_account, second_account = created_accounts
    deposit_request = DepositAccountRequest(accountId=first_account.id, amount=1000)
    funded_from_account = api_manager.user_steps.deposit_account(create_user_request, deposit_request)

    return funded_from_account, second_account
# первый объект → пополненный счёт с балансом 1000
# второй объект → пустой счёт с балансом 0

@pytest.fixture
def credit_account(
        account_factory: Callable[
            [CreateUserRequest],
            CreateAccountResponse
        ],
        credit_user_request: CreateUserRequest
) -> CreateAccountResponse:
    return account_factory(credit_user_request)

@pytest.fixture
def created_credit(
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        credit_account: CreateAccountResponse
) -> CreditResponse:
    credit_request = CreditRequest(
        accountId=credit_account.id,
        amount=5000,
        termMonths=12
    )
    credit_response = api_manager.user_steps.credit_request(credit_user_request, credit_request)

    return credit_response




