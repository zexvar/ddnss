from app.blueprints import BlueprintRegister


def register_blueprints(app, url_prefix=None):
    for bp in BlueprintRegister.import_blueprints():
        if url_prefix:
            bp.url_prefix = f"/{bp.url_prefix}/{url_prefix}"
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
