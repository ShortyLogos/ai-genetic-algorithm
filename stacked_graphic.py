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
    def __init__(self, categories):
        self._width = 700
        self._height = 300
        self._jobs = categories
        self._img = None 
        self.update_graphic()
    @property
    def image(self):
        return self._img
    @Slot()
    def update_graphic(self, ga=None):
        if ga: {
            'Worst': ga.history.history[:,1],
            'Average': ga.history.history[:,2],
            'Best': ga.history.history[:,0],
            }
        else:
            results = {
            'Worst': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            'Average': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            'Best': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            }

        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cumulated = data.cumsum(axis=1)
        category_colors = colormaps['tab20'](
            np.linspace(0.15, 0.85, data.shape[1]))
        dpi = 80
        figure = Figure(figsize=(self._width / dpi, self._height / dpi), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        for i, (colname, color) in enumerate(zip(self._jobs, category_colors)):
            widths = data[:, i]
            starts = data_cumulated[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
                            label=colname, color=color)
            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.bar_label(rects, label_type='center', color=text_color)
        
        ax.legend(ncol=int(len(self._jobs)/2), bbox_to_anchor=(-0.1, 1),
            loc=3, fontsize=7.5)
        canvas.draw()
        w, h = canvas.get_width_height()
        self._img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)

