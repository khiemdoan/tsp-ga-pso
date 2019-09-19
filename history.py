import time

import numpy as np
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class History:

    def __init__(self, viewport):
        self._viewport = viewport

        figure = Figure()
        self._canvas = FigureCanvas(figure)
        self._viewport.add(self._canvas)
        self._viewport.show_all()

    def draw(self, history):
        x = np.array([i + 1 for i in range(len(history))], dtype=np.int)
        y = np.array(history, dtype=np.float)

        figure = self._canvas.figure

        axis = figure.subplots(1, 1)
        axis.clear()
        axis.plot(x, y)

        self._canvas.draw()
        time.sleep(1e-2)
        figure.clf()
