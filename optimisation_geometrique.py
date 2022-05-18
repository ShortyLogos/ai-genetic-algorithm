import gaapp
from model.gacvm import Parameters, ProblemDefinition
from model.geometry_optimization import GeometryOptimizationProblem   #, ShapeGenerator
from uqtwidgets import create_scroll_int_value, QSimpleImage

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QComboBox, QPushButton, QLabel
from __feature__ import snake_case, true_property

class ShapePanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()
    shape_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QHBoxLayout()
        self.set_layout(self._main_layout)
        general_widget = QWidget()
        general_layout = QHBoxLayout(general_widget)
        self._shape_generator = ShapeGenerator()


        #### Parameters ####
        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)

        paramsForm_layout.add_row('Width', QLabel('500'))
        paramsForm_layout.add_row('Height', QLabel('250'))      
        
        self._shape_dropdown = QComboBox()
        self._shape_dropdown.add_item("Star 5",[5,0.5])
        self._shape_dropdown.add_item("Triangle",[3, 0])
        self._shape_dropdown.add_item("Square",[4, 0])
        self._shape_dropdown.add_item("Custom")
        self._shape_dropdown.currentIndexChanged.connect(self._shape_changed)
        paramsForm_layout.add_row('Shape', self._shape_dropdown)
        
        min_vertex = self._shape_generator.min_vertex
        max_vertex = self._shape_generator.max_vertex
        min_concavity = self._shape_generator.min_concavity
        max_concavity = self._shape_generator.max_concavity

        self._sides_widget, sides_layout = create_scroll_int_value(min_vertex, min_vertex, max_vertex, 1)
        paramsForm_layout.add_row('Numbers of vertex', sides_layout)
        self._concavity_widget, concavity_layout = create_scroll_int_value(min_concavity, min_concavity, max_concavity, 1)
        paramsForm_layout.add_row('Concavity Ratio', concavity_layout)
        self._sides_widget.valueChanged.connect(self.parameter_changed)
        self._concavity_widget.valueChanged.connect(self.parameter_changed)
        
        self._obstacle_widget, obstacle_layout = create_scroll_int_value(1, 30, 100, 1)
        paramsForm_layout.add_row('Obstacle count', obstacle_layout)
        self._obstacle_widget.valueChanged.connect(self.parameter_changed)
        
        button_obstacle = QPushButton("Generate obstacles")
        button_obstacle.clicked.connect(self.__generate)

        paramsBox_layout.add_widget(form_widget)
        paramsBox_layout.add_widget(button_obstacle)
        paramsBox_layout.add_stretch()

        #### Visualization ####
        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image = QSimpleImage()
        visuBox_layout.add_widget(self._image)

        general_layout.add_widget(paramsBox)
        general_layout.add_widget(visuBox)
        self._main_layout.add_widget(general_widget)

        self.parameter_changed.connect(self._update_adapter)

        #self._optimisation_problem = GeometryOptimizationProblem()

    @Slot()
    def _shape_changed(self):
        pass

    @Slot()
    def _update_adapter(self):
        #self._open_box_problem.box_width = (self._width_widget.value+10)/10
        #self._open_box_problem.box_height = (self._height_widget.value+10)/10
        pass

    @Slot()
    def __generate(self):
        pass

    @property
    def name(self):
        return "Optimisation Geometrique"

    @property
    def summary(self):
        return "Le but c'est de trouver la plus grosse forme qui rentre dans un nuage de points donné sans toucher à aucun point."

    @property
    def description(self):
        return "Je ferai la description pour les belles grosses formes plus tard"

    @property
    def problem_definition(self):
        '''
        Retourne un objet complet de définition du problème. L'objet retourné est celui qui sera résoud par l'algorithme génétique.
        '''
        return ProblemDefinition()

    @property
    def default_parameters(self):
        '''
        Retourne un objet de paramètres de l'algorithme génétique. Ces valeurs seront utilisée pour initialiser la liste des paramètres à gauche dans l'interface utilisateur.
        '''
        params = Parameters()
        return Parameters()


    def _update_from_simulation(self, ga=None):
        '''
        Fonction utilitaire permettant de donner du 'feedback' pour chaque pas de simulation. Il faut gérer le cas où ga est None. Lorsque ga est None, on donne un feedback d'initialisation sans aucune évolution.
        '''
