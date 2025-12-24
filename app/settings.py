import os
import tomllib

# basedir for instance_path
BASEDIR = os.path.abspath("data")
TOML_FILE = os.path.join(BASEDIR, "config.toml")


class CONFIG:
    DEBUG: bool = False

    AUTH_TOKEN: str = None
    AUTH_USERNAME: str = None
    AUTH_PASSWORD: str = None

    CLOUDFLARE_API_TOKEN: str = None

    SECRET_KEY: str = os.urandom(32).hex()
    DATABASE_URL: str = f"sqlite:///{BASEDIR}/data.db"

    @classmethod
    def load(cls):
        cls.load_toml()
        cls.load_env()
        return cls

    @classmethod
    def load_toml(cls):
        if not os.path.exists(TOML_FILE):
            return

        with open(TOML_FILE, "rb") as f:
            data = tomllib.load(f)

        for key, value in data.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

    @classmethod
    def load_env(cls):
        def convert_type(value: str, type):
            """Convert environment variable to the target type"""
            if type is bool:
                return value.lower() in ("true", "1", "yes")
            if type is int:
                return int(value)
            if type is float:
                return float(value)
            return value

        for key in dir(cls):
            if key.isupper() and key in os.environ:
                raw = os.environ[key]
                default = getattr(cls, key)
                cls_value = convert_type(raw, type(default))
                setattr(cls, key, cls_value)


CONFIG.load()
