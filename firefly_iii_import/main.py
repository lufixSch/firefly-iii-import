from firefly_iii_import import Config, DEFAULT_CONFIG_PATH, FireflyAPI, Transaction

from firefly_iii_client.model.transaction_type_property import TransactionTypeProperty

from argparse import ArgumentParser
from datetime import datetime


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to the config.toml",
        default=DEFAULT_CONFIG_PATH,
    )

    args = parser.parse_args()
    config = Config.load(args.config)

    firefly_api = FireflyAPI(config.firefly.host, config.firefly.token)

    firefly_api.create_transaction(
        Transaction(
            8,
            "Some Other Account",
            "N26",
            datetime(2022, 12, 1, 14, 10, 24),
            "Blackmail",
            "Another fun transaction",
            type=TransactionTypeProperty("deposit"),
        )
    )


if __name__ == "__main__":
    main()
