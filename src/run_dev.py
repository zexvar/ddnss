import yaml

from app import create_app

config = yaml.full_load(open("config-dev.yml"))
app = create_app(config)

if __name__ == "__main__":
    app.run(host="::", debug=True)
