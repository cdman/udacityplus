import webapp2
import globals
from src import urls


app = webapp2.WSGIApplication(urls.ROUTES, debug=globals.DEV)
