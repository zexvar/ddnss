import yaml


def init_app(app):
    app.config.update(yaml.full_load(open('app/config/config.yaml', 'r')))
