import importlib
from collections import deque
from pathlib import Path

from flask import Blueprint as FlaskBlueprint
from flask import Flask


class Blueprint(FlaskBlueprint):
    registry: list[FlaskBlueprint] = []

    def __new__(cls, *args, **kwargs):
        instance = FlaskBlueprint(*args, **kwargs)
        cls.registry.append(instance)
        return instance


def register_blueprints(app: Flask, scan_path=None):
    scan_path = Path(scan_path or f"{app.name}/blueprints")
    # Scan modules -- BFS
    queue = deque([scan_path])
    while queue:
        for file in queue.popleft().glob("*"):
            if file.name.startswith("__"):
                continue
            # Import file module or package module
            elif file.is_file() and file.suffix == ".py" or Path(file / "__init__.py").exists():
                module = ".".join(file.with_suffix("").parts)
                print(f"Import module: {module}")
                importlib.import_module(module)
            elif file.is_dir():
                queue.append(file)

    # Register `flask.Blueprint` on the app
    for bp in Blueprint.registry:
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
