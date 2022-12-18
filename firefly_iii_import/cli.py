from firefly_iii_import import Config, DEFAULT_CONFIG_PATH, FireflyAPI, Importer
from firefly_iii_import.loader import N26Loader
from datetime import datetime
import logging

# rom firefly_iii_client.model.transaction_type_property import TransactionTypeProperty

from argparse import ArgumentParser, Namespace


def _init_loader(config: Config):
    for bank in config.banks:
        if bank.type == "n26":
            yield N26Loader(bank)  # type: ignore


def list_transactions(args: Namespace):
    print(args)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(
        prog="Firefly III Importer",
        description="Import all transaction from different banks in a given timeframe.\
Alternatively auto import can be used. In this case the programm saves the last date and time of execution and imports all transactions since this date",
        epilog="Date and time inputs need to be formated in ISO 8601 format. \
Date: YYYY-MM-DD, \
Datetime: YYYY-MM-DDTHH:mm[+/-HH:mm]",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help=f"Path to the config.toml (If no value is provided the script searches for a f3i.config.toml at ./ and ~/) [{DEFAULT_CONFIG_PATH}]",
        default=DEFAULT_CONFIG_PATH,
    )

    parser.add_argument(
        "-f",
        "--from",
        type=datetime.fromisoformat,
        help="Start time limit for transactions If no value is provided the auto importer is used",
    )

    parser.add_argument(
        "-t",
        "--to",
        type=datetime.fromisoformat,
        help="End time limit for transactions. If no value is provided current date and time is used ('--from' needs to be defined)",
    )

    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Reset auto import to the current date",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List transactions instead of importing them (this will NOT update the last date and time of execution for the auto importer)",
    )

    args = parser.parse_args()

    config = Config.load(args.config)

    firefly_api = FireflyAPI(config.firefly.host, config.firefly.token)

    loader = _init_loader(config)

    importer = Importer([lo for lo in loader], firefly_api)

    if args.reset:
        return importer.reset_auto_import()

    start = args.__dict__["from"]
    if args.to and not start:
        raise Exception("Please provide a 'from' date as well when using the 'to' date")

    end = args.to if args.to else datetime.now()

    if args.list:
        return importer.list(start, end)

    if start:
        return importer.run(start, end)

    logging.info("Running auto importer")
    importer.auto_import()


if __name__ == "__main__":
    main()
