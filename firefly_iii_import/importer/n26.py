from firefly_iii_import.importer import BaseImporter
from firefly_iii_import import FireflyAPI


class N26Importer(BaseImporter):
    def __init__(self, username: str, password: str, firefly: FireflyAPI) -> None:
        pass

    def import_latest_transactions(self):
        pass
