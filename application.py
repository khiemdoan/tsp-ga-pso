from gi.repository import Gtk

from app_window import AppWindow


class Application(Gtk.Application):

    def __init__(self, app_id):
        super().__init__(application_id=app_id)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self)
        self.window.present()
