from datetime import datetime
from typing import List
from logging import warning, info, debug
from os import path

from firefly_iii_import.loader import BaseLoader
from firefly_iii_import import FireflyAPI

META_FILE_PATH = path.join(path.abspath(path.dirname(__file__)), "last_executed")


class Importer:
    def __init__(self, loader: List[BaseLoader], firely_api: FireflyAPI) -> None:
        self.loader = loader
        self.firefly_api = firely_api

    def _load_import_start(self):
        """Load start date and time for the auto import"""

        if not path.isfile(META_FILE_PATH):
            info(
                "----------------------------------------------------------------------------------------------------"
            )
            info(
                "Auto importer is executed the first time. 'last_executed' timestamp is created with current date"
            )
            info("The next time auto importer is executed it will start from this date")
            info(
                "----------------------------------------------------------------------------------------------------"
            )

            with open(META_FILE_PATH, "w+") as f:
                f.write(datetime.now().isoformat())

            return

        with open(META_FILE_PATH, "r") as f:
            return datetime.fromisoformat(f.readline())

    def auto_import(self):
        """Automatically import all transactions since the last time this function was executed"""

        start = self._load_import_start()

        if not start:
            return

        info(
            "----------------------------------------------------------------------------------------------------"
        )
        info(f"Running auto import from {start}")
        info(
            "----------------------------------------------------------------------------------------------------"
        )

        end = datetime.now()

        self.run(start, end)

        with open(META_FILE_PATH, "w") as f:
            f.write(end.isoformat())

    def reset_auto_import(self):
        """Reset auto import to the current date"""

        info(
            "----------------------------------------------------------------------------------------------------"
        )
        info(
            "Auto importer is reseted. 'last_executed' timestamp is overwritten with current date"
        )
        info("The next time auto importer is executed it will start from this date")
        info(
            "----------------------------------------------------------------------------------------------------"
        )

        with open(META_FILE_PATH, "w+") as f:
            f.write(datetime.now().isoformat())

    def run(self, start: datetime, end: datetime):
        """Load all transactions in the given timeframe from all given bank accounts and create a corresponding transaction in firefly"""

        for loader in self.loader:
            transactions = loader.load_transactions(start, end)

            info(
                f"Loaded {len(transactions)} transactions from account '{loader.config.name}'"
            )

            for transaction in transactions:
                try:
                    info(f"CREATE - {transaction}")
                    debug(transaction.__dict__)
                    self.firefly_api.create_transaction(transaction)
                    info("Transaction CREATED")
                except FireflyAPI.DuplicateTransactionError:
                    warning(
                        f"Duplicate transaction '{transaction.description}'"
                        + f"from '{transaction.source}' to '{transaction.destination}' - "
                        + f"Amount: {transaction.amount} {transaction.currency}"
                    )

    def list(self, start: datetime = None, end: datetime = None):
        """List transactions in the given timeframe"""

        if not start:
            start = self._load_import_start()

            if not start:
                return

        if not end:
            end = datetime.now()

        info(
            "----------------------------------------------------------------------------------------------------"
        )
        info(f"Listing all transactions between {start} and {end}")
        info(
            "----------------------------------------------------------------------------------------------------"
        )

        transactions = [
            transaction
            for loader in self.loader
            for transaction in loader.load_transactions(start, end)
        ]
        transactions.sort(key=lambda transaction: transaction.date)

        header = f"{'From':<35}{'To':<35}{'Amount':<15}{'Description':<30}"
        transactions = (
            f"{transaction.source:<35}{transaction.destination:<35}{f'{transaction.amount} {transaction.currency}':<15}{transaction.description:<30}"
            for transaction in transactions
        )

        print()
        print(header)
        print("".join(("-" for _ in range(35 + 35 + 15 + 30))))
        print("\n".join(transactions))
