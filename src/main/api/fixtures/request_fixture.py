import pytest
from pytest import FixtureRequest

from src.main.api.generators.bank_data_generator import BankDataGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.test_data.bank_rules import BankRules


@pytest.fixture
def deposit_request(
        created_account: CreateAccountResponse
) -> DepositAccountRequest:
    amount = BankDataGenerator.generate_amount(
        BankRules.DEPOSIT_MIN_AMOUNT,
        BankRules.DEPOSIT_MAX_AMOUNT
    )

    return DepositAccountRequest(
        accountId=created_account.id,
        amount=amount
    )

@pytest.fixture
def invalid_deposit_request(
        request: FixtureRequest,
        created_account: CreateAccountResponse
) -> DepositAccountRequest:
    return DepositAccountRequest(
        accountId=created_account.id,
        amount=request.param
    )

@pytest.fixture
def transfer_request(
        funded_accounts: tuple[
            DepositAccountResponse,
            CreateAccountResponse
        ]
) -> TransferAccountRequest:
    from_account, to_account = funded_accounts

    amount = BankDataGenerator.generate_amount(
        BankRules.TRANSFER_MIN_AMOUNT,
        from_account.balance
    )

    return TransferAccountRequest(
        fromAccountId=from_account.id,
        toAccountId=to_account.id,
        amount=amount
    )

@pytest.fixture
def invalid_transfer_request(
        request: FixtureRequest,
        funded_accounts: tuple[
            DepositAccountResponse,
            CreateAccountResponse
        ]
) -> TransferAccountRequest:
    from_account, to_account = funded_accounts

    return TransferAccountRequest(
        fromAccountId=from_account.id,
        toAccountId=to_account.id,
        amount=request.param
    )

@pytest.fixture
def credit_request(
        credit_account: CreateAccountResponse
) -> CreditRequest:
    amount = BankDataGenerator.generate_amount(
        BankRules.CREDIT_MIN_AMOUNT,
        BankRules.CREDIT_MAX_AMOUNT
    )
    term_months = BankDataGenerator.generate_integer(
        BankRules.CREDIT_MIN_TERM_MONTHS,
        BankRules.CREDIT_MAX_TERM_MONTHS
    )

    return CreditRequest(
        accountId=credit_account.id,
        amount=amount,
        termMonths=term_months
    )

@pytest.fixture
def invalid_credit_request(
        request: FixtureRequest,
        credit_account: CreateAccountResponse
) -> CreditRequest:
    return CreditRequest(
        accountId=credit_account.id,
        amount=request.param,
        termMonths=BankRules.CREDIT_MIN_TERM_MONTHS
    )

@pytest.fixture
def credit_repay_request(
        created_credit: CreditResponse
) -> CreditRepayRequest:
    return CreditRepayRequest(
        creditId=created_credit.creditId,
        accountId=created_credit.id,
        amount=created_credit.amount
    )

@pytest.fixture
def invalid_credit_repay_request(
        created_credit: CreditResponse
) -> CreditRepayRequest:
    return CreditRepayRequest(
        creditId=created_credit.creditId,
        accountId=created_credit.id,
        amount=(
            created_credit.amount - BankRules.AMOUNT_STEP
        )
    )
