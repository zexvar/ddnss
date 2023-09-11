import os

from dotenv import load_dotenv

basedir = os.path.join(os.getcwd(), "data")

load_dotenv()

CONFIG_ENV = os.getenv("CONFIG_ENV", "production")

DDNS_KEY = os.getenv("DDNS_KEY", None)

CLOUDFLARE_TOKEN = os.getenv("CF_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CF_ZONE_ID")
CLOUDFLARE_ZONE_NAME = os.getenv("CF_ZONE_NAME")


class Config(object):
    DDNS_KEY = DDNS_KEY
    CLOUDFLARE = {
        "TOKEN": CLOUDFLARE_TOKEN,
        "ZONE_ID": CLOUDFLARE_ZONE_ID,
        "ZONE_NAME": CLOUDFLARE_ZONE_NAME,
    }


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO: True
    DATABASE_URI = os.path.join(basedir, "data.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_URI}"


class ProductionConfig(Config):
    DATABASE_URI = os.path.join(basedir, "data.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_URI}"


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
