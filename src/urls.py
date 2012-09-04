import webapp2


ROUTES = [
    webapp2.Route('/', 'src.controllers.home.HomePage', name="home"),
]
