from app.utils import response


def register_error_handler(app):
    @app.errorhandler(404)
    def error_404(e: Exception):
        return response.error(str(e))

    @app.errorhandler(Exception)
    def error_default(e: Exception):
        return response.error(str(e))
