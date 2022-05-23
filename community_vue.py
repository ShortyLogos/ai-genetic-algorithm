import math
import gaapp
from model.gacvm import Parameters, ProblemDefinition

from PySide6.QtCore import Qt, Signal, Slot, QSignalBlocker
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QComboBox, QCheckBox
from uqtwidgets import create_scroll_int_value, QSimpleImage
from stacked_graphic import StackedBarWidget

from __feature__ import snake_case, true_property


class CommunityPanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()
    apply_custom = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QHBoxLayout()
        self.set_layout(self._main_layout)
        #self._problem = modeleProblem()        ######  Size et autres différents  ######

        #### Parameters ####
        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)   
        
        min_commu_size = 1 #self._problem.min_commu_size
        max_commu_size = 100 #self._problem.max_commu_size
        initial = math.ceil((max_commu_size-min_commu_size)/2)
        self._size_widget, size_layout = create_scroll_int_value(min_commu_size, initial, max_commu_size)
        self._size_widget.valueChanged.connect(self.parameter_changed)
        paramsForm_layout.add_row('Community Size', size_layout)

        self._context_dropdown = QComboBox()
        """
        for context in self._problem.context:
            self._context_dropdown.add_item(context.name, context.data)
        """
        self._context_dropdown.add_item("Custom")
        self._context_dropdown.currentIndexChanged.connect(self.__context_changed)
        paramsForm_layout.add_row('Context', self._context_dropdown)
        
        criterias = {
            'Pauvre': True,
            'Malade': True,
            'Egalitarian': False,
            'Violent': True,
            'Radioactif': True,
            'Monarchie': True
        } #self._problem.context.events
        
        paramsBox_layout.add_widget(form_widget)

        for key in criterias.keys():
            paramsBox_layout.add_widget(QCheckBox(key, self))
        
        paramsBox_layout.add_stretch()

        #### Visualization ####
        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image_visualization = QSimpleImage()
        categories = None #self._problem.jobs
        self._graphic_generator = StackedBarWidget(categories, 700, 300)
        visuBox_layout.add_widget(self._image_visualization)

        #### General layout and connections ####
        self._main_layout.add_widget(paramsBox)
        self._main_layout.add_widget(visuBox)
        self.parameter_changed.connect(self._update_problem)
        self.apply_custom.connect(self.__apply_custom)

    @Slot()
    def __context_changed(self, choice):
        signal_blocker = QSignalBlocker(self)
        custom_position = self._context_dropdown.count -1
        if choice != -1 and choice != custom_position:
            context = self._context_dropdown.item_data(choice)
            #self._custom2_widget.set_value(context[0])
            #self._custom1_widget.set_real_value(context[1])
            # ...
        self._update_problem()
        signal_blocker.unblock()

    @Slot()
    def __apply_custom(self):
        self._context_dropdown.set_current_index(self._context_dropdown.count-1)
        self.parameter_changed.emit()

    @Slot()
    def _update_problem(self):
        #self._problem.community_size = self._size_widget.value
        # ....
        pass 

    @property
    def name(self):
        return "Happy Community"

    @property
    def summary(self):
        return "Optimisation de la répartition des métiers au sein d'une communauté selon un context donné."

    @property
    def description(self):
        return "Je ferai la description pour la communauté plus tard"

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
        if ga:
            data = {
                'Best': self._problem.format_solution(ga.history.history[:,0]),
                'Average': self._problem.format_solution(ga.history.history[:,2]),
                'Worst': self._problem.format_solution(ga.history.history[:,1]),
                }
            self._graphic_generator.update_graphic(data)
            self._image_visualization = self._graphic_generator.image
