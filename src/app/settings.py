import os

from dotenv import load_dotenv

DATA_DIR = os.path.join(os.getcwd(), "data")
ENV_FILE = os.path.join(DATA_DIR, "config.env")

# load env
load_dotenv(ENV_FILE) if os.path.exists(ENV_FILE) else load_dotenv()

# get env
FLASK_ENV = os.getenv("FLASK_ENV", "production")


class Config(object):
    GUNICORN_BIND = "[::]:5000"
    GUNICORN_WORKERS = 2
    GUNICORN_WORKER_CLASS = "gevent"

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


configurations = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def init_config(flask_env: str):
    print(f"FLASK_ENV: {flask_env}")
    config = configurations.get(flask_env)
    for i in filter(lambda o: not str(o).startswith("_"), dir(config)):
        env_value = os.getenv(i)
        if env_value is not None:
            setattr(config, i, env_value)
        # print(f"{i}: {getattr(config, i)}")
    return config


config = init_config(FLASK_ENV)
