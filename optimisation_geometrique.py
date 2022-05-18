import gaapp
from model.gacvm import Parameters, ProblemDefinition
from model.geometry_optimization import GeometryOptimizationProblem, ShapeGenerator
from uqtwidgets import create_scroll_int_value, create_scroll_real_value, QSimpleImage

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QComboBox, QPushButton, QLabel
from __feature__ import snake_case, true_property

class ShapePanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()

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
        self._shape_dropdown.add_item("Triangle",[3, 0])
        self._shape_dropdown.add_item("Star 5",[5,0.5])
        self._shape_dropdown.add_item("Square",[4, 0])
        self._shape_dropdown.add_item("Custom")
        self._shape_dropdown.currentIndexChanged.connect(self.__shape_changed)
        paramsForm_layout.add_row('Shape', self._shape_dropdown)
        
        min_vertex = self._shape_generator.min_vertex_count
        max_vertex = self._shape_generator.max_vertex_count
        min_concavity = self._shape_generator.min_concavity
        max_concavity = self._shape_generator.max_concavity

        self._vertex_widget, vertex_layout = create_scroll_int_value(min_vertex, min_vertex, max_vertex)
        paramsForm_layout.add_row('Numbers of vertex', vertex_layout)
        self._vertex_widget.valueChanged.connect(self.parameter_changed)
        
        self._concavity_widget, concavity_layout = create_scroll_real_value(min_concavity, min_concavity, max_concavity, 2)
        paramsForm_layout.add_row('Concavity Ratio', concavity_layout)
        self._concavity_widget.valueChanged.connect(self.parameter_changed)
        
        self._obstacle_widget, obstacle_layout = create_scroll_int_value(1, 30, 100)
        paramsForm_layout.add_row('Obstacle count', obstacle_layout)
        self._obstacle_widget.valueChanged.connect(self.parameter_changed)
        
        button_obstacle = QPushButton("Generate obstacles")
        button_obstacle.clicked.connect(self.__generate_obstacles)

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

        self.parameter_changed.connect(self._update_problem)

        self._optimisation_problem = GeometryOptimizationProblem()

    """
        Le signal _update_problem doit utiliser les setter dans le GeometryOptimizationProblem
        Doit créer un autre signal qui va modifier les setter dans le ShapeGenerator
    """

    @Slot()
    def __shape_changed(self, choice):
        custom_position = self._shape_dropdown.count -1
        if choice != -1 and choice != custom_position:
            shape = self._shape_dropdown.item_data(choice)
            self._vertex_widget.set_value(shape[0])
            self._concavity_widget.set_real_value(shape[1])

    @Slot()
    def _update_problem(self):
        self._optimisation_problem.obstacles_count = self._obstacle_widget.value
        self._shape_generator.vertex_count = self._vertex_widget.value
        self._shape_generator.r = self._concavity_widget.value

    @Slot()
    def __generate_obstacles(self):
        #Basically ça va faire une image vide avec juste les obstacles dessus qui sera utiliser ensuite pour le reste de la simulation
        print("pleins de petits trous")
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
