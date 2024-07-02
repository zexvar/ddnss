from functools import wraps

from flask import jsonify, make_response, redirect, render_template, request


class BasicAuth:
    def __init__(self, app=None, enable=None, username=None, password=None, default_route=True):
        self._app = app
        self._enable = enable
        self._username = username
        self._password = password
        self._default_route = default_route
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._app = app

        if self._enable is None:
            self._enable = app.config.get("AUTH_ENABLE", False)

        if self._enable:
            self._username = app.config.get("AUTH_USERNAME", None)
            if self._username is None or len(self._username) == 0:
                raise ValueError("Missing required configuration for AUTH_USERNAME")

            self._password = app.config.get("AUTH_PASSWORD", None)
            if self._password is None or len(self._password) == 0:
                raise ValueError("Missing required configuration for AUTH_PASSWORD")

            import base64

            b64auth = base64.b64encode(f"{self._username}:{self._password}".encode())
            self._authorization = f"Basic {b64auth.decode()}"

            if self._default_route:
                self.add_default_route()

    def add_default_route(self):
        app = self._app

        # Add route for login
        @app.route("/login/", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                print(request.values)
                return render_template("/login.jinja")
            else:
                data = request.values
                if data.get("username") == self._username and data.get("password") == self._password:
                    resp = make_response(jsonify({"info": "Success!"}))
                    resp.set_cookie("authorization", self._authorization, max_age=3600)
                    return resp
                else:
                    return jsonify({"error": "Username or password error!"})

        # Add route for logout
        @app.route("/logout")
        def logout():
            resp = make_response(redirect("/login"))
            resp.delete_cookie("authorization")
            return resp

        return self

    def required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if self._enable:
                if not self.verify_auth():
                    return self.verify_error()
            return f(*args, **kwargs)

        return decorated

    def verify_auth(self):
        print("verify auth")
        auth = request.authorization
        if auth and auth.username == self._username and auth.password == self._password:
            print(auth.username, auth.password)
            return True
        elif request.cookies.get("authorization") == self._authorization:
            return True
        return False

    def verify_error(self):
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
