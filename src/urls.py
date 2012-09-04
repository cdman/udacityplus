import webapp2
from webapp2_extras import routes

ROUTES = [
    webapp2.Route('/', 'src.controllers.home.HomePage', name='home'),

    routes.PathPrefixRoute('/auth', [
        webapp2.Route('/login', 'src.controllers.authentication.Login', name='login'),
        webapp2.Route('/logout', 'src.controllers.authentication.Logout', name='logout'),
        webapp2.Route(
            '/openid/auth_complete',
            'src.controllers.authentication_openid.OpenIdAuthenticator',
            name='openid_auth_complete'),
    ]),
]

CRON_ROUTES = [
    routes.PathPrefixRoute('/cron', [
         webapp2.Route('/cleanup_sessions', 'src.controllers.cron.CleanupSessions'),
    ]),
]
