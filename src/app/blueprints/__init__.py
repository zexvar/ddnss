from importlib import import_module
from pathlib import Path

from flask import Blueprint as FlaskBlueprint


class BlueprintRegister:
    blueprints = []

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        instance = self._cls(*args, **kwargs)
        self.blueprints.append(instance)
        return instance

    @classmethod
    def import_blueprints(cls):
        for file in Path(__file__).parent.iterdir():
            if file.is_dir() or file.suffix == ".py":
                import_module(f"{__name__}.{file.stem}")
        return cls.blueprints


@BlueprintRegister
class Blueprint(FlaskBlueprint):
    pass
