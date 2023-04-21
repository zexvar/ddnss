import os
import yaml
import importlib
from flask_sqlalchemy import SQLAlchemy


def init(app):
    load_config(app)
    load_blueprint(app)
    db.init_app(app)


db = SQLAlchemy()


def load_config(app):
    app.config.update(yaml.full_load(open('config.yml', 'r')))


# 自动扫描加载蓝图
def load_blueprint(app):
    path = ['app', 'module']
    # app/module/
    for file in os.listdir('/'.join(path)):
        # app.module.xxx
        module_path = f'{path[0]}.{path[1]}.{file}'
        if file.startswith("__"):
            continue
        if file.endswith(".py"):
            module_path = module_path[:-3]
        module = importlib.import_module(module_path)
        app.register_blueprint(getattr(module, "bp"))
        print('Register blueprint: ' + module.__name__)
