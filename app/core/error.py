import traceback

from .resp import Html, Rest, response


def error_response(e, template, status=500):
    traceback.print_exception(e)
    return response(
        Rest.error(str(e), status=status),
        Html.render(template, status=status),
    )


def register_error_handler(app):
    @app.errorhandler(400)
    def error_400(e: Exception):
        return error_response(e, "errors/400.jinja", 400)

    @app.errorhandler(404)
    def error_404(e: Exception):
        return error_response(e, "errors/404.jinja", 404)

    @app.errorhandler(Exception)
    def error_500(e: Exception):
        return error_response(e, "errors/500.jinja")
