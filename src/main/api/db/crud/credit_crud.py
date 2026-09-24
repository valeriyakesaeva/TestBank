from sqlalchemy.orm import Session

from src.main.api.db.models.account_table import Account
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def delete_credits_by_account_id(db: Session, account_id: int) -> None:
        credits = db.query(Credit).filter(Credit.account_id == account_id).all()
        for credit in credits:
            db.delete(credit)
        db.commit()

    @staticmethod
    def get_credit_by_id(db: Session, credit_id: int) -> Credit | None:
        return db.query(Credit).filter(Credit.id == credit_id).first()

    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter(Credit.account_id == account_id).first()
