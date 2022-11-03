from datetime import datetime

from firefly_iii_client import Configuration, ApiClient, ApiException
from firefly_iii_client.api import transactions_api
from firefly_iii_client.model.transaction_store import TransactionStore
from firefly_iii_client.model.transaction_split_store import TransactionSplitStore
from firefly_iii_client.model.transaction_type_property import TransactionTypeProperty


class FireflyAPI:
    class Transaction:
        def __init__(self,
                     amount: int,
                     source: str,
                     destination: str,
                     date: datetime,
                     category: str = "",
                     description: str = "",
                     notes: str = "",
                     currency: str = "EUR",
                     type: TransactionTypeProperty = TransactionTypeProperty("TRANSFER")) -> None:
            self.amount = amount
            self.source = source
            self.destination = destination
            self.date = date
            self.category = category
            self.description = description
            self.notes = notes
            self.type = type

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
                            amount=transaction.amount,
                            category_name=transaction.category,
                            currency_code=transaction.currency,
                            date=transaction.date,
                            description=transaction.description,
                            destination_name=transaction.destination,
                            notes=transaction.notes,
                            source_name=transaction.source,
                            type=transaction.type,
                        )]
                )
                api_response = api_instance.store_transaction(transaction_store)
                print(api_response)
            except ApiException as e:
                print("Exception when calling AboutApi->get_about: %s\n" % e)
