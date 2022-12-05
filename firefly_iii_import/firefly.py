from datetime import datetime

from firefly_iii_client import Configuration, ApiClient, ApiException
from firefly_iii_client.api import transactions_api
from firefly_iii_client.model.transaction_store import TransactionStore
from firefly_iii_client.model.transaction_split_store import TransactionSplitStore
from firefly_iii_client.model.transaction_type_property import TransactionTypeProperty


class Transaction:
    def __init__(
        self,
        amount: int,
        source: str,
        destination: str,
        date: datetime,
        category: str = "",
        description: str = "",
        notes: str = "",
        currency: str = "EUR",
        type: TransactionTypeProperty = TransactionTypeProperty("transfer"),
    ) -> None:
        self.amount = amount
        self.source = source
        self.destination = destination
        self.date = date
        self.category = category
        self.description = description
        self.notes = notes
        self.type = type
        self.currency = currency


class FireflyAPI:
    class FireflyAPIError(Exception):
        pass

    class DuplicateTransactionError(Exception):
        def __init__(self, *args: object, transaction: Transaction) -> None:
            self.transaction = Transaction
            super().__init__(*args)

    def __init__(self, host, token) -> None:
        self.conf = Configuration(host, access_token=token)

    def create_transaction(self, transaction: Transaction):
        with ApiClient(self.conf) as client:
            api_instance = transactions_api.TransactionsApi(client)

            try:
                transaction_store = TransactionStore(
                    apply_rules=True,
                    error_if_duplicate_hash=True,
                    fire_webhooks=True,
                    transactions=[
                        TransactionSplitStore(
                            amount=str(transaction.amount),
                            category_name=transaction.category,
                            currency_code=transaction.currency,
                            date=transaction.date,
                            description=transaction.description,
                            destination_name=transaction.destination,
                            notes=transaction.notes,
                            source_name=transaction.source,
                            type=transaction.type,
                        )
                    ],
                )
                _ = api_instance.store_transaction(transaction_store)
            except ApiException as e:
                if body := getattr(e, "body", None):
                    print(body)

                    if (
                        body
                        == r'{"message":"Duplicate of transaction #6.","errors":{"transactions.0.description":["Duplicate of transaction #6."]}}'
                    ):
                        raise self.DuplicateTransactionError(
                            f"Duplicate of transaction '{transaction.description}' from '{transaction.source}' to '{transaction.destination}'",
                            transaction=transaction,
                        )

                raise self.FireflyAPIError(
                    "Exception when calling AboutApi->get_about: %s\n" % e
                )
