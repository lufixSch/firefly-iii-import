from abc import ABC
from datetime import datetime
from typing import List

from firefly_iii_import import Transaction
from firefly_iii_import.config import BankConfig


class BaseLoader(ABC):
    config: BankConfig

    def load_transactions(self, start: datetime, end: datetime) -> List[Transaction]:
        """Import the latest transactions"""

        return []
