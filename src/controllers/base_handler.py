import os
import webapp2
import jinja2
import globals


_TEMPLATES_DIR = os.path.join(globals.ROOT_DIRECTORY, 'templates')
_JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(_TEMPLATES_DIR), autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, vals={}):
        template = _JINJA_ENV.get_template("%s" % template)
        self.response.out.write(template.render(vals))
