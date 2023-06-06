import yaml

from app import create_app
from gevent import monkey

monkey.patch_all()

config = yaml.full_load(open('config.yml'))
app = create_app(config)
