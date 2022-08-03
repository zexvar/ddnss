import yaml
from flask import Flask

# import app.services

def create_app(app):
    app = Flask(__name__, static_url_path='')
    # services.init_app(app)
    return app

def config_app(app):
    data=yaml.full_load(open('app/config.yaml','r')) 
    auth=data['auth']
    app.auth=auth
    return app

app = None

if __name__ == '__main__':
    app = create_app(app)
    app = config_app(app)
    app.run(host='::', port=8000, debug=True)
