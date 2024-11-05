import os
import tomllib
from dataclasses import dataclass, field

from dotenv import load_dotenv

# basedir for instance_path
basedir = os.path.abspath("data")
env_file = os.path.join(basedir, "config.env")
toml_file = os.path.join(basedir, "config.toml")


@dataclass
class Config:
    DEBUG: bool = False

    CLOUDFLARE_TOKEN: str = None
    CLOUDFLARE_ZONE_ID: str = None
    CLOUDFLARE_ZONE_NAME: str = None

    AUTH_ENABLE: bool = None
    AUTH_USERNAME: str = None
    AUTH_PASSWORD: str = None

    DATABASE_URL: str = f"sqlite:///{basedir}/data.db"

    @staticmethod
    def convert_type(value: str, type):
        """Convert environment variable to the target type."""
        if type is bool:
            return value.lower() in ("true", "1", "yes")
        if type is int:
            return int(value)
        if type is float:
            return float(value)
        return value

    def __post_init__(self):
        # Override values with environment variables
        load_dotenv(env_file)
        for key in self.__annotations__.keys():
            v = os.getenv(key)
            if v is not None:
                type = self.__annotations__[key]
                setattr(self, key, self.convert_type(v, type))


# read toml config
with open(toml_file, "br") as f:
    toml_config = tomllib.load(f)

config = Config(**toml_config)
