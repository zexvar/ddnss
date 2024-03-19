import platform

print(f"Platform: {platform.system()}")
if platform.system() == "Linux":
    from gevent import monkey

    monkey.patch_all()

from app import create_app

app = create_app()
