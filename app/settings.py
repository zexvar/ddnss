import os
import tomllib
from dataclasses import dataclass

from dotenv import load_dotenv

# basedir for instance_path
BASEDIR = os.path.abspath("data")
ENV_FILE = os.path.join(BASEDIR, "config.env")
TOML_FILE = os.path.join(BASEDIR, "config.toml")


@dataclass
class Config:
    DEBUG: bool = False

    AUTH_ENABLE: bool = None
    AUTH_USERNAME: str = None
    AUTH_PASSWORD: str = None

    CLOUDFLARE_API_TOKEN: str = None

    DATABASE_URL: str = f"sqlite:///{BASEDIR}/data.db"

    @staticmethod
    def convert_type(value: str, type):
        """Convert environment variable to the target type"""
        if type is bool:
            return value.lower() in ("true", "1", "yes")
        if type is int:
            return int(value)
        if type is float:
            return float(value)
        return value

    def __post_init__(self):
        """Override values with environment variables"""
        for key in self.__annotations__.keys():
            value = os.getenv(key.upper())
            if value is not None:
                type = self.__annotations__[key]
                setattr(self, key, self.convert_type(value, type))


def load_config():
    # load env config
    if os.path.exists(ENV_FILE):
        load_dotenv(ENV_FILE)
    else:
        load_dotenv(verbose=True)

    # load toml config
    if os.path.exists(TOML_FILE):
        with open(TOML_FILE, "br") as f:
            return Config(**tomllib.load(f))
    else:
        return Config()


CONFIG = load_config()
