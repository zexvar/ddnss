import importlib
import os


# 自动注册蓝图
def init_app(app):
    for d in os.listdir('app/service/'):
        if d.endswith("Service.py"):
            services = importlib.import_module('app.service.' + d.replace('.py', ''))
            for obj in dir(services):
                if obj.endswith('_bp'):
                    # 读取蓝图对象
                    blueprint_object = getattr(services, obj)
                    app.register_blueprint(blueprint_object)
