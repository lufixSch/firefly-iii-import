import toml
from os import path

DEFAULT_CONFIG_PATH = path.join(
    path.dirname(path.dirname(path.abspath(__file__))), "config.toml"
)


class FireflyConfig:
    """Firefly configuration"""

    def __init__(self, host: str, token: str) -> None:
        self.host: str = host
        """ adress of the firefly host """

        self.token: str = token
        """ access token for the firefly instance """


class N26Config:
    """N26 configuration"""

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        """ n26 username/email"""

        self.password: str = password
        """ n26 password (do not share this with anyone)"""


class Config:

    firefly: FireflyConfig

    n26: N26Config

    @classmethod
    def load(cls, path: str):
        return cls(toml.load(path))

    def __init__(self, conf: dict) -> None:
        self.firefly = FireflyConfig(**conf.get("firefly", {}))
        self.n26 = N26Config(**conf.get("n26", {}))
