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


transactions = [
    {
        "id": "7cae12eb-9c67-3b2d-b41b-4f332171d58f",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "PT",
        "amount": -15.99,
        "currencyCode": "EUR",
        "originalAmount": -15.99,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "08006645451",
        "visibleTS": 1671349900727,
        "mcc": 5815,
        "mccGroup": 5,
        "merchantName": "APPLE.COM/BILL",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-media-electronics",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "referenceText": "-",
        "userCertified": 1671351567248,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671349900727,
        "merchantCountry": 5,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "7cae12eb-9c67-3b2d-b41b-4f332171d58f",
        "linkId": "7cae12eb-9c67-3b2d-b41b-4f332171d58f",
        "confirmed": 1671351567248,
    },
    {
        "id": "409e1bcd-af35-3bdd-9777-4a89b1a167c2",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "PT",
        "amount": -0.99,
        "currencyCode": "EUR",
        "originalAmount": -0.99,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "08006645451",
        "visibleTS": 1671349900727,
        "mcc": 5815,
        "mccGroup": 5,
        "merchantName": "APPLE.COM/BILL",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-media-electronics",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "referenceText": "-",
        "userCertified": 1671351567435,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671349900727,
        "merchantCountry": 5,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "409e1bcd-af35-3bdd-9777-4a89b1a167c2",
        "linkId": "409e1bcd-af35-3bdd-9777-4a89b1a167c2",
        "confirmed": 1671351567435,
    },
    {
        "id": "4589b810-7ce1-3035-a539-4dda6afecc23",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "AA",
        "amount": -36.29,
        "currencyCode": "EUR",
        "originalAmount": -36.29,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "800-279-6620",
        "visibleTS": 1671208594635,
        "mcc": 5942,
        "mccGroup": 13,
        "merchantName": "AMZN Mktp DE",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-shopping",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "userCertified": 1671208594663,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671208594635,
        "merchantCountry": 11,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "4589b810-7ce1-3035-a539-4dda6afecc23",
        "linkId": "4589b810-7ce1-3035-a539-4dda6afecc23",
        "confirmed": 1671208594663,
    },
    {
        "id": "c080a846-1d75-3b74-ad72-bfcce210ae40",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "AA",
        "amount": -487.34,
        "currencyCode": "EUR",
        "originalAmount": -487.34,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "Hirschau",
        "visibleTS": 1671207141385,
        "mcc": 5732,
        "mccGroup": 5,
        "merchantName": "www.conrad.de",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-media-electronics",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "userCertified": 1671207141411,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671207141385,
        "merchantCountry": 0,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "c080a846-1d75-3b74-ad72-bfcce210ae40",
        "linkId": "c080a846-1d75-3b74-ad72-bfcce210ae40",
        "confirmed": 1671207141411,
    },
    {
        "id": "528b2526-7d5c-11ed-b655-b6113d6054ae",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "CT",
        "amount": 200.0,
        "currencyCode": "EUR",
        "visibleTS": 1671207099366,
        "partnerName": "Von Sparkonto nach Hauptkonto",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-miscellaneous",
        "referenceText": "Lötstation",
        "userCertified": 1671207099381,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671207099366,
        "smartLinkId": "528b2526-7d5c-11ed-b655-b6113d6054ae",
        "linkId": "528b2526-7d5c-11ed-b655-b6113d6054ae",
        "paymentScheme": "SPACES",
        "confirmed": 1671207099381,
    },
    {
        "id": "6c3793c3-5257-3015-91b9-0ffd7c7d9728",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "AA",
        "amount": -118.08,
        "currencyCode": "EUR",
        "originalAmount": -118.08,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "800-279-6620",
        "visibleTS": 1671206730635,
        "mcc": 5942,
        "mccGroup": 13,
        "merchantName": "AMZN Mktp DE",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-shopping",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "userCertified": 1671206730663,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671206730635,
        "merchantCountry": 11,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "6c3793c3-5257-3015-91b9-0ffd7c7d9728",
        "linkId": "6c3793c3-5257-3015-91b9-0ffd7c7d9728",
        "confirmed": 1671206730663,
    },
    {
        "id": "3fbd1b13-4cc3-3979-a8ab-87714c760993",
        "userId": "08288b4e-3ba9-4729-b12d-7721d58d5682",
        "type": "PT",
        "amount": -17.99,
        "currencyCode": "EUR",
        "originalAmount": -17.99,
        "originalCurrency": "EUR",
        "exchangeRate": 1.0,
        "merchantCity": "Berlin",
        "visibleTS": 1671031697294,
        "mcc": 4899,
        "mccGroup": 5,
        "merchantName": "NETFLIX.COM",
        "accountId": "11df2a39-17f7-4756-aa13-ae881a3b90cb",
        "category": "micro-v2-media-electronics",
        "cardId": "ea618631-00a5-49cb-adaa-7d682a54c460",
        "referenceText": "-",
        "userCertified": 1671035166442,
        "pending": False,
        "transactionNature": "NORMAL",
        "createdTS": 1671031697294,
        "merchantCountry": 0,
        "txnCondition": "ECOMMERCE",
        "smartLinkId": "3fbd1b13-4cc3-3979-a8ab-87714c760993",
        "linkId": "3fbd1b13-4cc3-3979-a8ab-87714c760993",
        "confirmed": 1671035166442,
    },
]
