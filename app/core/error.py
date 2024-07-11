from app.utils import response


def register_error_handler(app):
    @app.errorhandler(400)
    def error_400(e: Exception):
        return response.resp("errors/400.jinja", e)

    @app.errorhandler(404)
    def error_404(e: Exception):
        return response.resp("errors/404.jinja", str(e))

    @app.errorhandler(500)
    def error_500(e: Exception):
        return response.resp("errors/500.jinja", str(e))

    @app.errorhandler(Exception)
    def error_default(e: Exception):
        return response.resp("errors/404.jinja", str(e))
