from collections import deque
from importlib import import_module
from inspect import getmembers
from pathlib import Path

from flask import Blueprint, Flask

_blueprints: set[Blueprint] = set()


def is_module(path: Path) -> bool:
    if path.is_file() and path.suffix == ".py":
        return True
    if path.is_dir() and (path / "__init__.py").is_file():
        return True
    return False


def path_to_module(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def register_blueprints(app: Flask, scan_path=None):
    scan_path = Path(scan_path or f"{app.name}/blueprints")
    # Scan modules with BFS
    queue = deque([scan_path])
    while queue:
        for path in queue.popleft().glob("*"):
            if path.name.startswith("__"):
                continue
            if path.is_dir():
                queue.append(path)

            # Import file or package module
            if is_module(path):
                module = import_module(path_to_module(path))
                print(f"[+] Import module: {module.__name__}")
                for _, member in getmembers(module):
                    if isinstance(member, Blueprint):
                        _blueprints.add(member)

    for bp in _blueprints:
        print(f"[+] Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
