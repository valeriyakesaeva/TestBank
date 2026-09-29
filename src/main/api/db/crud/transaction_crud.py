from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy import or_


class TransactionCrudDb:
    @staticmethod
    def delete_transactions_by_account_id(db: Session, account_id: int) -> None:
        transactions = db.query(Transaction).filter(or_(Transaction.to_account_id == account_id,
                                                       Transaction.from_account_id == account_id)).all()
        for transaction in transactions:
            db.delete(transaction)
        db.commit()
