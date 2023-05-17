from app import create_app
from gevent import monkey

monkey.patch_all()

app = create_app()

# gunicorn run
bind = "[::]:5000"
workers = 2
worker_class = "gevent"

# debug run
if __name__ == '__main__':
    app.run(host='::', debug=True)
