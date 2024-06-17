from importlib import import_module
from pathlib import Path

from flask import Blueprint


class BlueprintRegister:
    blueprints = []

    @classmethod
    def scan_modules(cls):
        for file in Path(__file__).parent.iterdir():
            if file.is_dir() or file.suffix == ".py":
                import_module(f"{__name__}.{file.stem}")

    @classmethod
    def register(cls, app, url_prefix=None):
        for bp in cls.blueprints:
            if url_prefix:
                bp.url_prefix = f"/{bp.url_prefix}/{url_prefix}"
            print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
            app.register_blueprint(bp)

    @classmethod
    def append(cls, blueprint: Blueprint):
        if isinstance(blueprint, Blueprint):
            cls.blueprints.append(blueprint)
            return blueprint


def new(blueprint: Blueprint):
    return BlueprintRegister.append(blueprint)


def register_blueprints(app, url_prefix=None):
    BlueprintRegister.scan_modules()
    BlueprintRegister.register(app, url_prefix)
