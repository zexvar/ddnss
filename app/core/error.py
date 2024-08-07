from .resp import Html, Rest, response


def error_response(e, template):
    return response(
        Rest.error(repr(e)),
        Html.render(template),
    )


def register_error_handler(app):
    @app.errorhandler(400)
    def error_400(e: Exception):
        return error_response(e, "errors/400.jinja")

    @app.errorhandler(404)
    def error_404(e: Exception):
        return error_response(e, "errors/404.jinja")

    @app.errorhandler(500)
    def error_500(e: Exception):
        return error_response(e, "errors/500.jinja")

    @app.errorhandler(Exception)
    def error_default(e: Exception):
        return error_response(e, "errors/500.jinja")
