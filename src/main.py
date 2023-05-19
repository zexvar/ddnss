from app import create_app
from gevent import monkey

# gevent
monkey.patch_all()

app = create_app()

if __name__ == '__main__':
    app.run(host='::', debug=True)
