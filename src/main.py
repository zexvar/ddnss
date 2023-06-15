import yaml
from gevent import monkey

from app import create_app

monkey.patch_all()

config = yaml.full_load(open("config.yml"))
app = create_app(config)
