from app import *

if __name__ == '__main__':
    app = create_app(app)
    app = config_app(app)
    app.run(host='::', port=8000, debug=True)