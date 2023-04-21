from app import create_app

app = create_app()

# gunicorn run
bind = "[::]:5000"
workers = 2
# worker_class = "sync"

# debug run
if __name__ == '__main__':
    app.run(host='::', debug=True)
