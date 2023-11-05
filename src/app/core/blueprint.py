from app.blueprints import scan_blueprint


def register_blueprints(app):
    for bp in scan_blueprint():
        print(f"Register blueprint: {bp.import_name} {bp.url_prefix}")
        app.register_blueprint(bp)
