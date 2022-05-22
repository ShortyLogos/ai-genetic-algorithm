import numpy as np

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from __feature__ import snake_case, true_property


class StackedBarWidget():
    def __init__(self, title, xLabel, yLabel):
        self._title = title
        self._x_label = xLabel
        self._y_label = yLabel
        self._colors =np.array([(1, 1, 0),(1, 0, 1),(1, 0, 0),(.2, .2, .2),(.5, .2, .2),(.2, .5, .2),(.2, .5, .2),(.7, 1, .7),(.7, .5, .7),(.5, 1, .7),(.7, 1, .5)])
        self.img = None
        self.update_graphic()

    @Slot()
    def update_graphic(self, width=500, height=250):
        dpi = 100

        ###################################
        figure = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111, projection='3d')
        ax.set_proj_type('persp')
        ###################################

        ax.set_title(self._title)
        ax.set_xlabel(self._x_label)
        ax.set_ylabel(self._y_label)

        canvas.draw()
        w, h = canvas.get_width_height()
        self.img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)