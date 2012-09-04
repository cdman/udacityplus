import globals
import gaesessions


def webapp_add_wsgi_middleware(app):
    app = gaesessions.SessionMiddleware(app, cookie_key=COOKIE_KEY)
    return app
