import numpy as np

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from __feature__ import snake_case, true_property

class StackedBarWidget():
    def __init__(self, xLabel, yLabel):
        self._x_label = xLabel
        self._y_label = yLabel
        self._mpl_widget = QLabel()
        self._colors =np.array([(1, 1, 0),(1, 0, 1),(1, 0, 0),(.2, .2, .2),(.5, .2, .2),(.2, .5, .2),(.2, .5, .2),(.7, 1, .7),(.7, .5, .7),(.5, 1, .7),(.7, 1, .5)])
        self._jobs = ['Doctor', 'Engineer', 'Farmer', 'Worker']
        self._results = {
            'Best': [10, 15, 17, 32],
            'Mean': [26, 22, 29, 10],
            'Worst': [35, 37, 7, 2]
        }
        self._img = self.update_graphic

    def image(self):
        return self._mpl_widget

    @Slot()
    def update_graphic(self, width=500, height=250):
        labels = list(self._results.keys())
        data = np.array(list(self._results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.colormaps['RdYlGn'](
            np.linspace(0.15, 0.85, data.shape[1]))
        ###################################
        width = 500
        height = 500
        dpi = 100
        figure = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        for i, (colname, color) in enumerate(zip(self._jobs, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
                            label=colname, color=color)
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncol=len(self._jobs), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
        canvas.draw()
        w, h = canvas.get_width_height()
        img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)
        self._mpl_widget.set_pixmap(QtGui.QPixmap.from_image(img))

