import importlib
import os


def register_blueprints(app):
    dot_path = ".".join(paths := [app.name, "blueprints"])
    for file in list(filter(lambda f: not str(f).startswith("__"), os.listdir(os.path.join(*paths)))):
        bp = getattr(importlib.import_module(dot_path + "." + file.removesuffix(".py")), "bp")
        bp.url_prefix = ("/" + bp.name) if bp.url_prefix is None else bp.url_prefix
        app.register_blueprint(bp)
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
