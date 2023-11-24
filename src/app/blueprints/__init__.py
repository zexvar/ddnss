from importlib import import_module
from pathlib import Path

from flask import Blueprint as BaseBlueprint

bp_list = []


class Blueprint(BaseBlueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = self.url_prefix or f"/{self.name}"
        bp_list.append(self)


def scan_blueprint():
    for file in Path(__file__).parent.iterdir():
        if file.is_dir() or file.suffix == ".py":
            import_module(f"{__name__}.{file.stem}")
    return bp_list
