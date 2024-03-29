######### Sommaire: Ce fichier contient tous les éléments reliés au problème un(openbox) pour le mettre dans le gaapp
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:13/05/2022
import gaapp
import math
from model.gacvm import Parameters, ProblemDefinition, GeneticAlgorithm
from model.openbox import OpenBoxProblem
from uqtwidgets import create_scroll_real_value, QSimpleImage
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout
from PySide6.QtGui import (QImage, QPainter, QPen, QColor, QBrush)
from __feature__ import snake_case, true_property

class BoxPanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QHBoxLayout()
        self.set_layout(self._main_layout)
        
        self._open_box_problem = OpenBoxProblem()

        #### Parameters ####
        min_value = self._open_box_problem.min_box_size
        max_value = self._open_box_problem.max_box_size
        initial = math.ceil((max_value-min_value)/2)
        precision = 1

        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)
        self._width_widget, width_layout = create_scroll_real_value(min_value, initial, max_value, precision)
        self._height_widget, height_layout = create_scroll_real_value(min_value, initial, max_value, precision)
        paramsForm_layout.add_row('Width', width_layout)
        paramsForm_layout.add_row('Height', height_layout)
        self._width_widget.valueChanged.connect(self.parameter_changed)
        self._height_widget.valueChanged.connect(self.parameter_changed)
        paramsBox_layout.add_stretch()
        paramsBox_layout.add_widget(form_widget)
        paramsBox_layout.add_stretch()

        #### Visualization ####
        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image_visualization = QSimpleImage()
        visuBox_layout.add_widget(self._image_visualization)

        #### General Layout and connections ####
        self._main_layout.add_widget(paramsBox)
        self._main_layout.add_widget(visuBox)
        self.parameter_changed.connect(self._update_adapter)

    @Slot()
    def _update_adapter(self):
        self._open_box_problem.box_width = self._width_widget.get_real_value()
        self._open_box_problem.box_height = self._height_widget.get_real_value()
        
    @Slot()
    def _draw_image(self, cut):
        max_image_size = min(self._image_visualization.width, self._image_visualization.height)
        cut = (cut/self._open_box_problem.max_box_size) * max_image_size
        box_width = (self._open_box_problem.box_width / self._open_box_problem.max_box_size) * max_image_size
        box_height = (self._open_box_problem.box_height / self._open_box_problem.max_box_size) * max_image_size
        qimage = QImage(box_width, box_height, QImage.Format_ARGB32)
        qimage.fill(QColor(154,123,98))
        painter = QPainter(qimage)
        painter.set_brush(QColor(64, 64, 64))

        painter.set_pen(QPen(QColor(64, 64, 64), 3, Qt.DotLine))
        # On fait cut*2 pour des raisons esthétiques afin de réussir notre effet visuel de découpe
        # autrement on aperçoit la boîte du fond derrière les pointillés externes
        painter.draw_rect(0, 0, cut, cut)
        painter.draw_rect(0, box_height-cut, cut, cut*2)
        painter.draw_rect(box_width-cut, 0, cut*2, cut)
        painter.draw_rect(box_width-cut, box_height-cut, cut*2, cut*2)
        painter.end()
        self._image_visualization.image = qimage

    @property
    def name(self):
        return "Open Box"

    @property
    def summary(self):
        return "Permet de déterminer l'aire des quatre coins à découper de la boîte afin d'optimiser son volume une fois assemblée."

    @property
    def description(self):
        return "Membres:\n" \
                "\tJean-Christophe Caron\n" \
                "\tSamuel Horvath\n" \
                "\tDéric Marchand\n" \
                "\tKarl Robillard Marchand\n"\
                "\nL'objectif consiste à obtenir le volume maximale d'une boîte en déterminant l'aire d'un coin à découper." \
                "\n------------------------------------------------" \
                "\nProblème à 1 dimension :"\
                "\nUn côté des coins à découper (0 à la taille ls plus petite entre la hauteur et la largeur de la boîte, divisé par deux)."\

    @property
    def problem_definition(self):
        '''
        Retourne un objet complet de définition du problème. L'objet retourné est celui qui sera résoud par l'algorithme génétique.
        '''
        return ProblemDefinition(self._open_box_problem.domains, self._open_box_problem)

    @property
    def default_parameters(self):
        #Voir les lignes 364 à 372 pour contenus des parametres, objet parametre du model
        '''
        Retourne un objet de paramètres de l'algorithme génétique. Ces valeurs seront utilisée pour initialiser la liste des paramètres à gauche dans l'interface utilisateur.
        '''
        params = Parameters()
        params.maximum_epoch = 150
        params.mutation_rate = 0.6
        return params

    def _update_from_simulation(self, ga=None):
        '''
        Fonction utilitaire permettant de donner du 'feedback' pour chaque pas de simulation. Il faut gérer le cas où ga est None. Lorsque ga est None, on donne un feedback d'initialisation sans aucune évolution.
        '''
        if ga:
            #Appelé à chaque evolution, on recoit tout l'engin, accès à toute la population 
            cut = ga.history.best_solution[0]
            self._draw_image(cut)
        else:
            pass #Appelé soit quand l'evolution evolue ou pas, si pas, ga à none