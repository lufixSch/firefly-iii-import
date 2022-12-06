import toml
from typing import Literal, List

from os import path


def _create_default_path():
    cnf_path = "f3i.config.toml"
    if path.isfile(cnf_path):
        return path.abspath(cnf_path)

    cnf_path = path.join(path.expanduser("~"), cnf_path)
    if path.isfile(cnf_path):
        return cnf_path

    return ""


DEFAULT_CONFIG_PATH = _create_default_path()
"""Default path to config.toml"""

BANK_TYPES = Literal["n26"]
"""Different bank types which can be used in the config.toml"""


class FireflyConfig:
    """Firefly configuration"""

    def __init__(self, host: str, token: str) -> None:
        self.host: str = host
        """ adress of the firefly host """

        self.token: str = token
        """ access token for the firefly instance """


class BankConfig:
    """Basic Bank config"""

    @classmethod
    def from_type(cls, type: BANK_TYPES, **kwargs):
        if type == "n26":
            return N26Config(**kwargs)

        return cls(bank_type=type, **kwargs)

    def __init__(self, type: BANK_TYPES, name: str, **kwargs) -> None:
        self.type = type
        self.name = name

        for key in kwargs:
            setattr(self, key, kwargs[key])


class N26Config(BankConfig):
    """N26 configuration"""

    type: BANK_TYPES = "n26"

    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        device_token: str,
        mfa_type: Literal["sms", "app"],
        store_login_data: bool,
    ) -> None:
        self.name: str = name
        """ name of the account in your Firefly III instance"""

        self.username: str = username
        """ n26 username/email"""

        self.password: str = password
        """ n26 password (do not share this with anyone)"""

        self.device_token: str = device_token
        """ custom generated UID wich identifies your device (python -c 'import uuid; print(uuid.uuid4())')"""

        self.mfa_type: Literal["sms", "app"] = mfa_type
        """ Type of multi factor authentication"""

        self.store_login_data: bool = store_login_data
        """ Wether the login data should be stored in order to avoid MFA every time the script is executed"""


class Config:
    """firefly_iii_import configuration"""

    firefly: FireflyConfig
    """ Location and access token for the Firefly III instance"""

    banks: List[BankConfig] = []
    """ List of configurations for all different bank accounts"""

    @classmethod
    def load(cls, path: str):
        """Load configuration from .toml file"""

        return cls(toml.load(path))

    def __init__(self, conf: dict) -> None:
        self.firefly = FireflyConfig(**conf["firefly"])

        if bank_confs := conf.get("banks", None):
            for bank_conf in bank_confs:
                self.banks.append(BankConfig.from_type(**bank_conf))
