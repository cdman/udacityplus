import globals
import gaesessions
import secrets


def webapp_add_wsgi_middleware(app):
    app = gaesessions.SessionMiddleware(app, cookie_key=secrets.SESSION_KEY)
    return app
