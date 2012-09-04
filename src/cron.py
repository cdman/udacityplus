import globals
import gaesessions

from src.controllers import base_handler


class CleanupSessions(base_handler.BaseHandler):
    def get(self):
        while not gaesessions.delete_expired_sessions():
            pass
