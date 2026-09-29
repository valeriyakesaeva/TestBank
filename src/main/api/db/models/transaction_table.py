from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from src.main.api.db.base import Base
from src.main.api.db.models.account_table import Account
from src.main.api.db.models.credit_table import Credit

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey('account.id'), nullable=True)
    from_account_id = Column(Integer, ForeignKey('account.id'), nullable=True)
    credit_id = Column(Integer, ForeignKey('credit.id'), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f'<Transaction(id={self.id}, to_account_id={self.to_account_id}, '
                f'from_account_id={self.from_account_id}, credit_id={self.credit_id}, '
                f'amount={self.amount}, transaction_type={self.transaction_type}, created_at={self.created_at})>')
