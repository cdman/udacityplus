from src.controllers import base_handler

class HomePage(base_handler.BaseHandler):
    def get(self):
        template_values = {'title' : 'my title'}
        self.render("index.html", template_values)
