import gaapp
from model.gacvm import Parameters, ProblemDefinition

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout
from __feature__ import snake_case, true_property

class BoxPanel(gaapp.QSolutionToSolvePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_layout(QHBoxLayout())
        # self.general_widget = 
        
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
        return ProblemDefinition()

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
