import os
import importlib
from flask_sqlalchemy import SQLAlchemy


def init(app):
    init_blueprint(app)
    db.init_app(app)


db = SQLAlchemy()


# 扫描并注册蓝图
def init_blueprint(app):
    path = ['app', 'blueprints']
    dir_path = '/'.join(path)  # app/blueprints/xxx
    mod_path = '.'.join(path)  # app.blueprints.xxx
    for file in os.listdir(dir_path):
        if file.startswith('__'):
            continue
        if file.endswith('.py'):
            file = file[:-3]
        module = importlib.import_module(f'{mod_path}.{file}')
        app.register_blueprint(getattr(module, 'bp'))
        print(f'Register blueprint: {module.__name__}')
