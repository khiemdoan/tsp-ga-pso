import time
from threading import Lock

import numpy as np
from gi.repository import Gtk
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

lock = Lock()


class Map:

    def __init__(self, viewport: Gtk.Viewport):
        self._viewport = viewport

        figure = Figure()
        self._canvas = FigureCanvas(figure)
        self._viewport.add(self._canvas)
        self._viewport.show_all()

    def draw_cities(self, cities, tour=False):
        x = np.array([city.x for city in cities], dtype=np.float)
        y = np.array([city.y for city in cities], dtype=np.float)

        figure = self._canvas.figure

        axis = figure.subplots(1, 1)
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)

        axis.clear()

        axis.scatter(x, y, color='red', linewidth=0.5)

        if tour:
            x = np.append(x, x[0])
            y = np.append(y, y[0])
            axis.plot(x, y, linewidth=0.5)

        self._canvas.draw()
