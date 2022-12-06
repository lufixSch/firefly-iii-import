from firefly_iii_import.loader import BaseLoader
from firefly_iii_import import Transaction
from firefly_iii_import.config import N26Config

from firefly_iii_client.model.transaction_type_property import TransactionTypeProperty

from datetime import datetime
from typing import List, Dict, Any
from logging import info
from os import path

from n26.api import Api
from n26.config import Config
from n26.const import ATM_WITHDRAW

DATA_STORE_PATH = path.join(path.abspath(path.dirname(__file__)), "n26_login_store")


class N26Loader(BaseLoader):
    def __init__(self, config: N26Config) -> None:
        self.config = config

        conf = Config(validate=False)
        conf.USERNAME.value = config.username
        conf.PASSWORD.value = config.password
        conf.LOGIN_DATA_STORE_PATH.value = (
            path.join(DATA_STORE_PATH, config.username)
            if config.store_login_data
            else None
        )
        conf.MFA_TYPE.value = config.mfa_type
        conf.DEVICE_TOKEN.value = config.device_token
        conf.validate()

        self.client = Api(conf)

        info(
            f"Authenticating N26 account {config.username}. Please approve the login using the selected MFA type"
        )
        self.client.get_account_info()

    def load_transactions(self, start: datetime, end: datetime):
        transactions: List[Dict[str, Any]] = self.client.get_transactions(
            from_time=int(start.timestamp() * 1000),
            to_time=int(end.timestamp() * 1000),
            limit=10000,
        )  # type: ignore

        return [
            Transaction(
                amount=abs(n26_trans["amount"]),
                source=self.config.name
                if n26_trans["amount"] <= 0
                else n26_trans.get("partnerName", ""),
                destination=n26_trans.get(
                    "partnerName", n26_trans.get("merchantName", "")
                )
                if n26_trans["amount"] <= 0
                else self.config.name,
                date=datetime.fromtimestamp(int(n26_trans["visibleTS"] / 1000)),
                category=" & ".join(
                    [
                        cat.capitalize()
                        for cat in n26_trans["category"].lstrip("micro-v2-").split("-")
                    ]
                ),
                description="ATM Withdrawal"
                if n26_trans["type"] == ATM_WITHDRAW
                else n26_trans["referenceText"],
                currency=n26_trans["currencyCode"],
                foreign_amount=n26_trans.get("originalAmount", None),
                foreign_currency=n26_trans.get("originalCurrency", "EUR"),
                type=TransactionTypeProperty(
                    "withdrawal" if n26_trans["amount"] <= 0 else "deposit"
                ),
            )
            for n26_trans in transactions
        ]
