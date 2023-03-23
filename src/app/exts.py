import os
import yaml
import importlib
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


def init(app):
    read_config(app)
    scan_blueprint(app)
    db.init_app(app)
    bootstrap.init_app(app)


db = SQLAlchemy()
bootstrap = Bootstrap()


def read_config(app):
    app.config.update(yaml.full_load(open('config.yml', 'r')))


# 自动扫描注册蓝图
def scan_blueprint(app):
    path = ['app', 'module']
    # app/blueprint/
    for file in os.listdir('/'.join(path)):
        # app.blueprint.xxx
        module_path = f'{path[0]}.{path[1]}.{file}'
        if file.endswith(".py"):
            module_path = module_path[:-3]
        elif file == '__pycache__':
            continue
        module = importlib.import_module(module_path)
        bp = getattr(module, "bp")
        print('Register blueprint: ' + module.__name__)
        app.register_blueprint(bp)
