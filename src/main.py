import platform

if platform.system() == "Linux":
    from gevent import monkey
    from gunicorn.app.base import BaseApplication

    monkey.patch_all()

    class Application(BaseApplication):
        def __init__(self, app, config):
            self.app = app
            self.config = config
            super().__init__()

        def load_config(self):
            CONFIG = self.config
            self.cfg.set("bind", CONFIG.GUNICORN_BIND)
            self.cfg.set("workers", CONFIG.GUNICORN_WORKERS)
            self.cfg.set("worker_class", CONFIG.GUNICORN_WORKER_CLASS)

        def load(self):
            return self.app


from app import config, create_app

app = create_app()


print(f"Platform: {platform.system()}")
if __name__ == "__main__":
    (Application(app, config).run() if platform.system() == "Linux" else app.run(host="::"))
