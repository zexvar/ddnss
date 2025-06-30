import os
import tomllib
from dataclasses import dataclass

# basedir for instance_path
BASEDIR = os.path.abspath("data")
TOML_FILE = os.path.join(BASEDIR, "config.toml")


@dataclass
class Config:
    DEBUG: bool = False

    AUTH_TOKEN: str = None
    AUTH_USERNAME: str = None
    AUTH_PASSWORD: str = None

    CLOUDFLARE_API_TOKEN: str = None

    SECRET_KEY: str = os.urandom(32).hex()
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


def load_config() -> Config:
    if os.path.exists(TOML_FILE):
        with open(TOML_FILE, "rb") as f:
            return Config(**tomllib.load(f))
    return Config()


CONFIG = load_config()
