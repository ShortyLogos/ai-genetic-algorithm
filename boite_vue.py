import gaapp
from model.gacvm import Parameters, ProblemDefinition, GeneticAlgorithm
from model.openbox import OpenBoxProblem
from uqtwidgets import create_scroll_real_value, QSimpleImage

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QLabel
from __feature__ import snake_case, true_property

class BoxPanel(gaapp.QSolutionToSolvePanel):
    
    parameter_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QHBoxLayout()
        self.set_layout(self._main_layout)
        general_widget = QWidget()
        general_layout = QHBoxLayout(general_widget)

        minValue = 1
        maxValue = 10
        precision = 1

        paramsBox = QGroupBox("Parameters")
        paramsBox_layout = QVBoxLayout(paramsBox)
        form_widget = QWidget()
        paramsForm_layout = QFormLayout(form_widget)
        self._width_widget, width_layout = create_scroll_real_value(minValue, 10, maxValue, precision)
        self._height_widget, height_layout = create_scroll_real_value(minValue, 5, maxValue, precision)
        paramsForm_layout.add_row('Width', width_layout)
        paramsForm_layout.add_row('Height', height_layout)
        self._width_widget.valueChanged.connect(self.parameter_changed)
        self._height_widget.valueChanged.connect(self.parameter_changed)
        paramsBox_layout.add_stretch()
        paramsBox_layout.add_widget(form_widget)
        paramsBox_layout.add_stretch()

        visuBox = QGroupBox("Visualization")
        visuBox_layout = QHBoxLayout(visuBox)
        self._image = QSimpleImage()
        visuBox_layout.add_widget(self._image)

        general_layout.add_widget(paramsBox)
        general_layout.add_widget(visuBox)
        self._main_layout.add_widget(general_widget)

        self.parameter_changed.connect(self._update_adapter)

        self._open_box_problem = OpenBoxProblem()


    @Slot()
    def _update_adapter(self):
        self._open_box_problem.box_width = (self._width_widget.value+10)/10
        self._open_box_problem.box_height = (self._height_widget.value+10)/10
        
    @property
    def name(self):
        return "Boite Ouverte"

    @property
    def summary(self):
        return "Le but de cette problématique est de construire l'architecture idéale pour une boite possédant le plus grand volume considérant des mesures définis par l'usager."

    @property
    def description(self):
        return "Je ferai la description de la boite magique plus tard"

    @property
    def problem_definition(self):
        '''
        Retourne un objet complet de définition du problème. L'objet retourné est celui qui sera résoud par l'algorithme génétique.
        '''
        new_problem = ProblemDefinition(self._open_box_problem.domains, self._open_box_problem)
        genetic_algorithm = GeneticAlgorithm(new_problem)
        genetic_algorithm.is_ready
        genetic_algorithm.evolve()
        genetic_algorithm.population
        return new_problem

    @property
    def default_parameters(self):
        #Voir les lignes 364 à 372 pour contenus des parametres, objet parametre du model
        '''
        Retourne un objet de paramètres de l'algorithme génétique. Ces valeurs seront utilisée pour initialiser la liste des paramètres à gauche dans l'interface utilisateur.
        '''
        params = Parameters()
        params.maximum_epoch = 100
        return params

    def _update_from_simulation(self, ga=None):
        '''
        Fonction utilitaire permettant de donner du 'feedback' pour chaque pas de simulation. Il faut gérer le cas où ga est None. Lorsque ga est None, on donne un feedback d'initialisation sans aucune évolution.
        '''






"""

Voir le dessin avec les calculs et tout de ses exemples.

Faire boucle for i in range(n) n=nbr côtés. 
Calculé l'angle theta = 2pie/n. x=cos(théta) et y=sin(théta) 

Pour étoiles: 
faire boucle for i in range(n) n=nbr côtés
(calculer 2 "thétas" pour coin interne et externe)
théta R = i*2pie/n => Coin externe
théta r = théta R + 1/2*2pie/n => Coin interne
x-pointe= cost R
y-pointe= sin R
append(xR, yR)
xc= (cost Théta r) * r
yc = (sin Théta r) * r
append(xc,yc)

"""