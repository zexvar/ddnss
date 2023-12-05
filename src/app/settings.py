import os

from dotenv import load_dotenv

DATA_DIR = os.path.join(os.getcwd(), "data")
ENV_FILE = os.path.join(DATA_DIR, "config.env")

# load env
load_dotenv(ENV_FILE) if os.path.exists(ENV_FILE) else load_dotenv()

# get env
FLASK_ENV = os.getenv("FLASK_ENV", "production")


class Config(object):
    CLOUDFLARE_TOKEN = None
    CLOUDFLARE_ZONE_ID = None
    CLOUDFLARE_ZONE_NAME = None

    DDNS_KEY = None


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATA_DIR}/data.db"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO: True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO: True
    TESTING = True


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(flask_env: str):
    print(f"FLASK_ENV: {flask_env}")

    for i in filter(lambda o: not str(o).startswith("_"), dir(configs.get(flask_env))):
        env_value = os.getenv(i)
        if env_value is not None:
            setattr(configs, i, env_value)
        print(f"{i}: {getattr(configs, i)}")

    return configs


config = get_config(FLASK_ENV)
