from abc import ABC


class BaseImporter(ABC):
    def import_latest_transactions(self):
        """Import the latest transactions"""
