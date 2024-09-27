from collections import deque
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


def register_blueprints(app: Flask, root_path=Path(__file__).parent):
    # Scan modules -- BFS
    queue = deque([root_path.relative_to(Path.cwd())])
    while queue:
        current = queue.popleft()
        for file in current.glob("*"):
            if file.name.startswith("__"):
                continue
            elif (file.is_file() and file.suffix == ".py") or (file.is_dir() and (file / "__init__.py").exists()):
                module = ".".join(file.with_suffix("").parts)
                print(f"Import module: {module}")
                import_module(module)
            elif file.is_dir():
                queue.append(file)

    # Register `flask.Blueprint` on the app
    for bp in Blueprint.registry:
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
