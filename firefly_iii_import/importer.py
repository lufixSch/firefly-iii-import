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

    def auto_import(self):
        """Automatically import all transactions since the last time this function was executed"""

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
            start = datetime.fromisoformat(f.readline())

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
