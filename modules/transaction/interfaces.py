from abc import abstractmethod, ABC
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Sequence

from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.models import Transaction


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    async def update(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    async def delete(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[Transaction]:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        pass

    @abstractmethod
    async def get_by_name_and_wallet_and_type(
        self, name: str, wallet_id: int, transaction_date: date
    ) -> Transaction | None:
        pass

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        pass

    @abstractmethod
    async def get_by_wallet_id(
        self, wallet_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        pass

    @abstractmethod
    async def get_by_subject_id(
        self, subject_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        pass

    @abstractmethod
    async def get_sum_value_by_type_and_user_id(
        self,
        user_id: int,
        transaction_type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        pass

    @abstractmethod
    async def get_sum_value_by_wallet_id_and_type(
        self,
        wallet_id: int,
        transaction_type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        pass
