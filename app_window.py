import threading
import time

from gi.repository import Gtk

from algorithms import GeneticAlgorithm
from data_reader import DataReader
from history import History
from map import Map
from models import CostMap


@Gtk.Template(filename='ui/window.glade')
class AppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = 'AppWindow'

    dataset_desciption = Gtk.Template.Child('dataset_description')
    map_viewport = Gtk.Template.Child('map_viewport')
    history_viewport = Gtk.Template.Child('history_viewport')
    n_iteration = Gtk.Template.Child('n_iteration')
    second_per_iteration = Gtk.Template.Child('second_per_iteration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = Map(self.map_viewport)
        self.history = History(self.history_viewport)
        self._cities = []

        self._cost_map = None
        self._algorithm = None
        self._alg_thread = None
        self._pause = False

        self._ga_history = []

    @Gtk.Template.Callback()
    def select_data_file(self, button):
        data_path = button.get_file().get_path()
        reader = DataReader()
        reader.load(data_path)

        description = reader.get_description()
        self.dataset_desciption.set_text(description)

        self._cities = reader.get_cities()

        self.map.draw_cities(self._cities)

        if self._alg_thread:
            self._alg_thread.join()
            self._alg_thread = None

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, button):
        self._pause = False
        if not self._alg_thread:
            self._alg_thread = threading.Thread(target=self.execute_thread, daemon=True)
            self._cost_map = CostMap(self._cities)
            self._algorithm = GeneticAlgorithm(self._cities, self._cost_map)
        self._alg_thread.start()

    @Gtk.Template.Callback()
    def on_pause_button_clicked(self, button):
        self._pause = True

    def execute_thread(self):
        if not self._algorithm:
            return

        n_iteration = self.n_iteration.get_text()
        n_iteration = int(n_iteration)

        for i in range(n_iteration):
            self._algorithm.iterate()

            cities = [self._cities[o] for o in self._algorithm.best.order]
            self.map.draw_cities(cities, True)

            cost = self._algorithm.best.cost
            self._ga_history.append(cost)
            self.history.draw(self._ga_history)

            print(f'{i + 1} - {cost}')
            time.sleep(float(self.second_per_iteration.get_text()))
