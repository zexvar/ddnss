from importlib import import_module
from pathlib import Path

from flask import Blueprint as FlaskBlueprint
from flask import Flask


class Blueprint(FlaskBlueprint):
    registry: list[FlaskBlueprint] = []

    def __new__(cls, *args, **kwargs):
        instance = FlaskBlueprint(*args, **kwargs)
        cls.registry.append(instance)
        return instance


def register_blueprints(app: Flask, url_prefix=None):
    # Scan modules
    for file in Path(__file__).parent.iterdir():
        if file.is_dir() or file.suffix == ".py":
            import_module(f"{__name__}.{file.stem}")

    # Register `flask.Blueprint` on the app
    for bp in Blueprint.registry:
        if url_prefix:
            bp.url_prefix = f"/{bp.url_prefix}/{url_prefix}"
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
