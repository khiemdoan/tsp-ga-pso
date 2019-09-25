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

    def draw(self, ga_history, pso_history):
        x_ga = np.array([i + 1 for i in range(len(ga_history))], dtype=np.int)
        y_ga = np.array(ga_history, dtype=np.float)

        x_pso = np.array([i + 1 for i in range(len(pso_history))], dtype=np.int)
        y_pso = np.array(pso_history, dtype=np.float)

        figure = self._canvas.figure

        axis = figure.subplots(1, 1)
        axis.clear()
        ga, = axis.plot(x_ga, y_ga)
        pso, = axis.plot(x_pso, y_pso)
        axis.legend((ga, pso), ('GA', 'PSO'))

        self._canvas.draw()
        time.sleep(1e-2)
        try:
            figure.clf()
        except:
            pass
