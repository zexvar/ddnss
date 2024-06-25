import os

from dotenv import load_dotenv

# basedir for instance_path
basedir = os.path.abspath("data")

# load env
load_dotenv(os.path.join(basedir, "config.env"))


class BaseConfig(object):
    CLOUDFLARE_TOKEN = None
    CLOUDFLARE_ZONE_ID = None
    CLOUDFLARE_ZONE_NAME = None

    DATABASE_URL = None

    AUTH_ENABLE = None
    AUTH_USERNAME = None
    AUTH_PASSWORD = None

    def __init__(self) -> None:
        for k in filter(lambda o: not str(o).startswith("_"), dir(self)):
            v = os.getenv(k)
            if v is not None:
                setattr(self, k, v)
            # print(f"[CONFIG FROM ENV] {k}: {v}")


class ProductionConfig(BaseConfig):
    DATABASE_URL = f"sqlite:///{basedir}/data.db"


class DevelopmentConfig(BaseConfig):
    DATABASE_URL = f"sqlite:///{basedir}/test.db"
    DEBUG = True


class TestingConfig(BaseConfig):
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True
    TESTING = True


# load config
FLASK_ENV = os.getenv("FLASK_ENV", "production")
print(f"FLASK_ENV: {FLASK_ENV}")


def load_config() -> BaseConfig:
    match FLASK_ENV:
        case "development":
            return DevelopmentConfig()
        case "production":
            return ProductionConfig()
        case "testing":
            return TestingConfig()


config = load_config()
