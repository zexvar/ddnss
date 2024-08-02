from functools import wraps

from flask import Flask, jsonify, make_response, redirect, render_template, request


class Auth:
    @classmethod
    def init_app(cls, app: Flask, enable=None, username=None, password=None, default_route=True):
        cls._app = app
        cls._enable = enable
        cls._username = username
        cls._password = password
        cls._default_route = default_route

        if cls._enable is None:
            cls._enable = app.config.get("AUTH_ENABLE", False)

        if cls._enable:
            cls._username = app.config.get("AUTH_USERNAME", None)
            if cls._username is None or len(cls._username) == 0:
                raise ValueError("Missing required configuration for AUTH_USERNAME")

            cls._password = app.config.get("AUTH_PASSWORD", None)
            if cls._password is None or len(cls._password) == 0:
                raise ValueError("Missing required configuration for AUTH_PASSWORD")

            import base64

            b64auth = base64.b64encode(f"{cls._username}:{cls._password}".encode())
            cls._authorization = f"Basic {b64auth.decode()}"

            if cls._default_route:
                cls.add_default_route()

    @classmethod
    def add_default_route(cls):
        app = cls._app

        # Add route for login
        @app.route("/login/", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                print(request.values)
                return render_template("/login.jinja")
            else:
                data = request.values
                if data.get("username") == cls._username and data.get("password") == cls._password:
                    resp = make_response(jsonify({"info": "Success!"}))
                    resp.set_cookie("authorization", cls._authorization, max_age=3600)
                    return resp
                else:
                    return jsonify({"error": "Username or password error!"})

        # Add route for logout
        @app.route("/logout")
        def logout():
            resp = make_response(redirect("/login"))
            resp.delete_cookie("authorization")
            return resp

        return cls

    @classmethod
    def required(cls, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if cls._enable:
                if not cls.verify_auth():
                    return cls.verify_error()
            return f(*args, **kwargs)

        return decorated

    @classmethod
    def verify_auth(cls):
        print("verify auth")
        auth = request.authorization
        if auth and auth.username == cls._username and auth.password == cls._password:
            print(auth.username, auth.password)
            return True
        elif request.cookies.get("authorization") == cls._authorization:
            return True
        return False

    @classmethod
    def verify_error(cls):
        accept = request.headers.get("accept", "*/*")
        # html response
        if "text/html" in accept:
            return render_template("/login.jinja")
        # auth response
        else:
            """Sends a 401 response that enables basic auth"""
            resp = make_response(jsonify({"message": "Login required!"}), 401)
            resp.headers = {"WWW-Authenticate": 'Basic realm="nologin"'}
            return resp


def register_auth_handler(app):
    Auth.init_app(app)
