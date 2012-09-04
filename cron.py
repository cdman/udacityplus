import webapp2
import globals
from src import urls


app = webapp2.WSGIApplication(urls.CRON_ROUTES, debug=globals.DEV)
