from app.blueprints import BlueprintRegister


def register_blueprints(app, url_prefix=None):
    BlueprintRegister.scan_modules()
    BlueprintRegister.register(app, url_prefix)
