import webapp2

from src.controllers import base_handler
from src.controllers import authentication_openid


class Login(base_handler.BaseHandler):
    def get(self):
        return webapp2.redirect(
            authentication_openid.OpenIdAuthenticator(None, None).prepare_authentication_request())


class Logout(base_handler.BaseHandler):
    def get(self):
        template_values = {'title' : 'my title'}
        self.render("index.html", template_values)
