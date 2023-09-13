import os
from importlib import import_module

from flask import Blueprint


def register_blueprints(app):
    basepath = f"{app.name}.blueprints"
    for file in os.listdir(basepath.replace(".", "/")):
        if not file.startswith("__"):
            module = import_module(f"{basepath}.{file}".removesuffix(".py"))
            register_module_bp(module, app)


def register_module_bp(module, app):
    bp = getattr(module, "bp", None)
    if isinstance(bp, Blueprint):
        if bp.url_prefix is None:
            bp.url_prefix = f"/{bp.name}"
        app.register_blueprint(bp)
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
    return None
