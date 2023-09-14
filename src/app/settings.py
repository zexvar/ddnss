import os

from dotenv import load_dotenv

# basedir
basedir = os.path.join(os.getcwd(), "data")

ENV_URI = os.path.join(basedir, "config.env")
DATABASE_URI = os.path.join(basedir, "data.db")

# load env
if os.path.exists(ENV_URI):
    load_dotenv(ENV_URI)
else:
    load_dotenv()


# get env
CONFIG_ENV = os.getenv("CONFIG_ENV", "production")

CLOUDFLARE_TOKEN = os.getenv("CF_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CF_ZONE_ID")
CLOUDFLARE_ZONE_NAME = os.getenv("CF_ZONE_NAME")

DDNS_KEY = os.getenv("DDNS_KEY", None)


class Config(object):
    DDNS_KEY = DDNS_KEY
    CLOUDFLARE = {
        "TOKEN": CLOUDFLARE_TOKEN,
        "ZONE_ID": CLOUDFLARE_ZONE_ID,
        "ZONE_NAME": CLOUDFLARE_ZONE_NAME,
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_URI}"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO: True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO: True
    TESTING = True


config_env = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

config = config_env[CONFIG_ENV]
