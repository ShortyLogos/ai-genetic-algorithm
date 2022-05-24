######### Sommaire: Ce fichier dessine le graphique pour notre troisième problème(happy_community)
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:23/05/2022
######### Référence: https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import colormaps

from __feature__ import snake_case, true_property

class StackedBarWidget():
    def __init__(self, categories, width=500, height=250):
        self._width = width
        self._height = height
        self._categories = categories
        self._img = None 

    @property
    def image(self):
        return self._img
    
    @Slot()
    def update_graphic(self, data=None):
        if data:
            labels = list(data.keys())
            data = np.array(list(data.values()))
            
            data_cumulated = data.cumsum(axis=1)
            category_colors = colormaps['tab20'](
                np.linspace(0.01, 1, data.shape[1]))
            
            dpi = 80
            figure = Figure(figsize=(self._width / dpi, self._height / dpi), dpi=dpi)
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            ax.invert_yaxis()
            ax.xaxis.set_visible(False)
            ax.set_xlim(0, np.sum(data, axis=1).max())

            for i, (colname, color) in enumerate(zip(self._categories, category_colors)):
                widths = data[:, i]
                starts = data_cumulated[:, i] - widths
                rects = ax.barh(labels, widths, left=starts, height=0.5,
                                label=colname, color=color)
                r, g, b, _ = color
                text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
                ax.bar_label(rects, label_type='center', color=text_color, alpha=0)

            ax.legend(ncol=int(len(self._categories)/2), bbox_to_anchor=(-0.1, 1),
                loc=3, fontsize=7.5)
            
            canvas.draw()
            w, h = canvas.get_width_height()
            self._img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)
