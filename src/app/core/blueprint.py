from importlib import import_module
from pathlib import Path

from flask import Blueprint


def register_blueprints(app, bp_dir="blueprints"):
    for file in Path(f"{app.name}/{bp_dir}").iterdir():
        module_name = file.stem
        if not str(module_name).startswith("__"):
            module = import_module(f"{app.name}.{bp_dir}.{module_name}")
            register_module_bp(module, app)


def register_module_bp(module, app):
    bp = vars(module).get("bp")
    if isinstance(bp, Blueprint):
        if bp.url_prefix is None:
            bp.url_prefix = f"/{bp.name}"
        app.register_blueprint(bp)
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
    return None
