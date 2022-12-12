from .cloudflare import Cloudflare


def init(app):
    Cloudflare.load(app.config['cloudflare'])