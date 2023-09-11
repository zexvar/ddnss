import platform

from app import create_app

if platform.system() == "Linux":
    from gevent import monkey

    monkey.patch_all()

app = create_app()

if __name__ == "__main__":
    app.run(host="::")
