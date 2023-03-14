import importlib
import os


# 自动注册蓝图
def init(app):
    path = ['app','blueprint']
    # app/blueprint/
    for file in os.listdir('/'.join(path)):
        if file.endswith("_bp.py"):
            # app.blueprint.xxx_bp
            bp_module = importlib.import_module(f'{path[0]}.{path[1]}.{file}'[:-3])
            bp_obj = getattr(bp_module, "bp")
            print('Register blueprint: '+bp_module.__name__)
            app.register_blueprint(bp_obj)

