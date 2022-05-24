######### Sommaire: Ce fichier contient tous les éléments reliés au problème deux(geometry_optimization) pour le mettre dans le gaapp
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:18/05/2022
import gaapp
from model.gacvm import Parameters, ProblemDefinition
from model.geometry_optimization import GeometryOptimizationProblem, ShapeGenerator
from uqtwidgets import create_scroll_int_value, create_scroll_real_value, QSimpleImage

from PySide6.QtCore import Qt, Signal, Slot, QSignalBlocker
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QComboBox, QPushButton, QLabel
from PySide6.QtGui import (QImage, QPainter, QPen, QColor, QTransform)
from __feature__ import snake_case, true_property

class ShapePanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()
    apply_custom = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QHBoxLayout()
        self.set_layout(self._main_layout)
        self._shape_generator = ShapeGenerator()
        self._optimisation_problem = GeometryOptimizationProblem()

        #### Parameters ####
        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)

        self._image_width = self._optimisation_problem.surface.width()
        self._image_height = self._optimisation_problem.surface.height()

        paramsForm_layout.add_row('Width', QLabel(str(self._image_width)))
        paramsForm_layout.add_row('Height', QLabel(str(self._image_height)))      
        
        self._shape_dropdown = QComboBox()
        presets = self._shape_generator.preset_shapes
        for shape in presets.keys():
            self._shape_dropdown.add_item(shape, presets[shape])
        self._shape_dropdown.add_item("Custom")
        self._shape_dropdown.currentIndexChanged.connect(self.__shape_changed)
        paramsForm_layout.add_row('Shape', self._shape_dropdown)
        
        min_vertex = self._shape_generator.min_vertex_count
        max_vertex = self._shape_generator.max_vertex_count
        self._vertex_widget, vertex_layout = create_scroll_int_value(min_vertex, min_vertex, max_vertex)
        paramsForm_layout.add_row('Vertex Count', vertex_layout)
        self._vertex_widget.valueChanged.connect(self.apply_custom)
        
        min_concavity = self._shape_generator.min_concavity
        max_concavity = self._shape_generator.max_concavity
        self._concavity_widget, concavity_layout = create_scroll_real_value(min_concavity, min_concavity, max_concavity, 2)
        paramsForm_layout.add_row('Concavity Ratio', concavity_layout)
        self._concavity_widget.valueChanged.connect(self.apply_custom)
        
        min_obstacle = self._optimisation_problem.min_obstacles
        start_obstacle = self._optimisation_problem.obstacles_count
        max_obstacle = self._optimisation_problem.max_obstacles
        self._obstacle_widget, obstacle_layout = create_scroll_int_value(min_obstacle, start_obstacle, max_obstacle)
        paramsForm_layout.add_row('Obstacles Count', obstacle_layout)
        self._obstacle_widget.valueChanged.connect(self.parameter_changed)
        
        button_obstacle = QPushButton("Generate Obstacles")
        button_obstacle.clicked.connect(self._generate_obstacles)

        paramsBox_layout.add_widget(form_widget)
        paramsBox_layout.add_widget(button_obstacle)
        paramsBox_layout.add_stretch()

        #### Visualization ####
        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image_visualization = QSimpleImage()
        visuBox_layout.add_widget(self._image_visualization)

        #### General layout and connections ####
        self._main_layout.add_widget(paramsBox)
        self._main_layout.add_widget(visuBox)
        
        self.parameter_changed.connect(self._update_problem)
        self.apply_custom.connect(self.__apply_custom)

    @Slot()
    def __shape_changed(self, choice):
        signal_blocker = QSignalBlocker(self)
        custom_position = self._shape_dropdown.count -1
        if choice != -1 and choice != custom_position:
            shape = self._shape_dropdown.item_data(choice)
            self._vertex_widget.set_value(shape[0])
            self._concavity_widget.set_real_value(shape[1])
        self._update_problem()
        signal_blocker.unblock()

    @Slot()
    def __apply_custom(self):
        self._shape_dropdown.set_current_index(self._shape_dropdown.count-1)
        self.parameter_changed.emit()

    @Slot()
    def _update_problem(self):
        self._optimisation_problem.obstacles_count = self._obstacle_widget.value
        self._shape_generator.vertex_count = self._vertex_widget.value
        self._shape_generator.r = self._concavity_widget.get_real_value()

    @Slot()
    def _generate_obstacles(self):
        self._optimisation_problem.generate_obstacles()
        self._draw_image()

    @Slot()
    def _draw_image(self, ga=None):
        qimage = QImage(self._image_width, self._image_height, QImage.Format_ARGB32)
        qimage.fill(QColor(0,0,0))
        for obstacle in self._optimisation_problem.obstacles:
            painter = QPainter(qimage)
            painter.set_brush(Qt.white)
            painter.set_pen(QPen(Qt.white, 2))
            painter.draw_point(obstacle)
            painter.end()
        if ga:
            for chromosone in ga.population:
                self._draw_shape(qimage, chromosone)
            self._draw_shape(qimage, ga.history.best_solution, True)
        self._image_visualization.image = qimage

    @Slot()
    def _draw_shape(self, qimage, transformations, best=False):
        t = QTransform()
        t.translate(transformations[0], transformations[1])
        t.rotate(transformations[2])
        t.scale(transformations[3], transformations[3])
        modified_poly = t.map(self._optimisation_problem.polygon)
        painter = QPainter(qimage)
        if best:
            painter.set_brush(QColor(176, 33, 33))
            painter.set_pen(QColor(255, 0, 0))
            painter.draw_polygon(modified_poly, Qt.OddEvenFill)
        else:
            painter.set_brush(Qt.NoBrush)
            painter.set_pen(QColor(122, 55, 122))
            painter.draw_polygon(modified_poly, Qt.OddEvenFill)
        painter.end()       

    @Slot()
    def _generate_shape(self):
        self._shape_generator.generate_shape()
        self._optimisation_problem.polygon = self._shape_generator.shape

    @property
    def name(self):
        return "Geometry Optimization Problem"

    @property
    def summary(self):
        return "Maximisez l'aire possible d'une forme de votre choix, selon un nombre d'obstacles déterminés à l'intérieur d'une surface."

    @property
    def description(self):
        return  "Membres:\n" \
                "\tJean-Christophe Caron\n" \
                "\tSamuel Horvath\n" \
                "\tDéric Marchand\n" \
                "\tKarl Robillard Marchand\n"\
                "\nL'objectif consiste à obtenir la plus grande aire possible d'une forme donnée, tout en s'assurant que celle-ci" \
                "ne touche à aucun obstacle ni ne dépasse la surface. L'usager peut choisir une forme prédéfinie (triangle, carré, étoile à cinq branches). " \
                "Il peut également générer une forme personnalisée en spécifiant le nombre de sommets et le ratio de concavité. Il est également possible de" \
                "générer un nombre d'obtacles déterminés.\n" \
                "\n------------------------------------------------" \
                "\nProblème à 4 dimensions:"\
                "\nTranslation en X (0 à la largeur de la surface)"\
                "\nTranslation en Y (0 à la hauteur de la surface)" \
                "\nRotation (0 à 360 degrés)" \
                "\nRotation (0 à 360 degrés)" \

    @property
    def problem_definition(self):
        '''
        Retourne un objet complet de définition du problème. L'objet retourné est celui qui sera résoud par l'algorithme génétique.
        '''
        self._generate_shape()
        return ProblemDefinition(self._optimisation_problem.domains, self._optimisation_problem)

    @property
    def default_parameters(self):
        '''
        Retourne un objet de paramètres de l'algorithme génétique. Ces valeurs seront utilisée pour initialiser la liste des paramètres à gauche dans l'interface utilisateur.
        '''
        params = Parameters()
        return params

    def _update_from_simulation(self, ga=None):
        '''
        Fonction utilitaire permettant de donner du 'feedback' pour chaque pas de simulation. Il faut gérer le cas où ga est None. Lorsque ga est None, on donne un feedback d'initialisation sans aucune évolution.
        '''
        if ga:
            self._draw_image(ga)
        else:
            pass