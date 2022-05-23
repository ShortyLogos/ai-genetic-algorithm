######### Sommaire: Ce fichier contient tous les éléments reliés au problème trois(happy_community) pour le mettre dans le gaapp
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:23/05/2022
import math
import gaapp
from model.gacvm import Parameters, ProblemDefinition
from model.happy_community import HappyCommunityProblem

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
        self._problem = HappyCommunityProblem()

        #### Parameters ####
        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)   
        
        self._context_dropdown = QComboBox()
        context_list = self._problem.context.preset_gui_contexts
        for key in context_list.keys():
            self._context_dropdown.add_item(key, context_list[key])
        self._context_dropdown.add_item("Custom")
        self._context_dropdown.currentIndexChanged.connect(self.__context_changed)
        paramsForm_layout.add_row('Context', self._context_dropdown)

        min_commu_size = self._problem.context.community_min_size
        max_commu_size = self._problem.context.community_max_size
        initial = self._problem.context.community_size
        self._size_widget, size_layout = create_scroll_int_value(min_commu_size, initial, max_commu_size)
        self._size_widget.valueChanged.connect(self.parameter_changed)
        paramsForm_layout.add_row('Community Size', size_layout)

        min_life_expectancy = self._problem.context.socio_political_context.life_expectancy_min
        max_life_expectancy = self._problem.context.socio_political_context.life_expectancy_max
        initial = self._problem.context.socio_political_context.life_expectancy
        self._life_widget, life_layout = create_scroll_int_value(min_life_expectancy, initial, max_life_expectancy)
        self._life_widget.valueChanged.connect(self.apply_custom)
        paramsForm_layout.add_row('Life Expectancy', life_layout)
 
        min_scroll = self._problem.context.min_trait_value
        max_scroll = self._problem.context.max_trait_value
        initial = self._problem.context.default_trait_value
        
        self._religious_widget, religious_layout = create_scroll_int_value(min_scroll, initial, max_scroll)
        self._religious_widget.valueChanged.connect(self.apply_custom)
        paramsForm_layout.add_row('Religious Sentiment', religious_layout)
        self._domestic_widget, domestic_layout = create_scroll_int_value(min_scroll, initial, max_scroll)
        self._domestic_widget.valueChanged.connect(self.apply_custom)
        paramsForm_layout.add_row('Domestic Stability', domestic_layout)
        self._education_widget, education_layout = create_scroll_int_value(min_scroll, initial, max_scroll)
        self._education_widget.valueChanged.connect(self.apply_custom)
        paramsForm_layout.add_row('Education Rate', education_layout)

        paramsBox_layout.add_widget(form_widget)

        self.__checkbox_list = []
        criterias = self._problem.context.socio_political_context.events
        for key in criterias.keys():
            checkbox = QCheckBox(key, self)
            checkbox.toggled.connect(self.apply_custom)
            self.__checkbox_list.append(checkbox)
            paramsBox_layout.add_widget(checkbox)
        
        paramsBox_layout.add_stretch()

        #### Visualization ####
        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image_visualization = QSimpleImage()
        self._graphic_generator = StackedBarWidget(self._problem.jobs_tags, 700, 300)
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
            self._life_widget.set_value(context[0])
            self._religious_widget.set_value(context[1])
            self._domestic_widget.set_value(context[2])
            self._education_widget.set_value(context[3])
            for i in range(len(self.__checkbox_list)):
                self.__checkbox_list[i].set_checked(context[i+4])
        self._update_problem()
        signal_blocker.unblock()

    @Slot()
    def __apply_custom(self):
        self._context_dropdown.set_current_index(self._context_dropdown.count-1)
        self.parameter_changed.emit()

    @Slot()
    def _update_problem(self):
        self._problem.context.community_size = self._size_widget.value
        self._problem.context.socio_political_context.life_expectancy = self._life_widget.value
        self._problem.context.set_community_trait('Religious Sentiment', self._religious_widget.value)
        self._problem.context.set_community_trait('Domestic Stability', self._domestic_widget.value)
        self._problem.context.set_community_trait('Education Rate', self._education_widget.value)
        for checkbox in self.__checkbox_list:
            self._problem.context.socio_political_context.set_event(checkbox.text, checkbox.check_state()) 

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
        return ProblemDefinition(self._problem.domains, self._problem)

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
