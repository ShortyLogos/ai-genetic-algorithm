import random
import numpy as np
import model.gacvm as gacvm
import model.umath as umath
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform
from __feature__ import snake_case, true_property


class HappyCommunityProblem:
    def __init__(self, community_context, community_size=200):
        self.__community_context = community_context
        self.__community_size = community_size
        self.__priorities = None  # array des coefficients de pondération selon le contexte
        # méthode generate_priorities(community_context) ?
        self.__domains = gacvm.Domains(np.array([
            0
        ], float),
            ('doctor', 'engineer', 'farmer', 'worker'))
        self.generate_jobs()

    @property
    def community_context(self):
        return self.__community_context

    @community_context.setter
    def community_context(self, new_community):
        self.__community_context = new_community

    def __call__(self, jobs):
        pass

    def generate_jobs(self):
        pass

class SocioPoliticalContext:
    def __init__(self, life_expectancy=60):
        self.__life_expectancy = life_expectancy
        self.__cultural_shift = False
        self.__economic_crisis = False
        self.__political_instability = False
        self.__war_raging = False
        self.__global_warming = False
        self.__epidemic = False

    @property
    def life_expectancy(self):
        return self.__life_expectancy

    @life_expectancy.setter
    def life_expectancy(self, val):
        self.__life_expectancy = val

    @property
    def cultural_shift(self):
        return self.__cultural_shift

    @cultural_shift.setter
    def cultural_shift(self, bool):
        self.__cultural_shift = bool

    @property
    def economic_crisis(self):
        return self.__economic_crisis

    @economic_crisis.setter
    def economic_crisis(self, bool):
        self.__economic_crisis = bool

    @property
    def political_instability(self):
        return self.__political_instability

    @political_instability.setter
    def political_instability(self, bool):
        self.__political_instability = bool

    @property
    def war_raging(self):
        return self.__war_raging

    @war_raging.setter
    def war_raging(self, bool):
        self.__war_raging = bool

    @property
    def global_warming(self):
        return self.__global_warming

    @global_warming.setter
    def global_warming(self, bool):
        self.__global_warming = bool

    @property
    def epidemic(self):
        return self.__global_warming

    @epidemic.setter
    def epidemic(self, bool):
        self.__global_warming = bool

class CommunityContext:
    def __init__(self, socio_political_context):
        # Les indices sont calculé de 0 à 10
        # On doit faire appel à des setters pour les paramétrer
        self.__religious_sentiment = 0
        self.__domestic_stability = 0
        self.__education_rate = 0
        # Ci-dessous, les priorités d'une communauté (moyenne pondérée dont la somme = 1)
        self.__community_cost = 0
        self.__health = 0
        self.__food_production = 0
        self.__goods_production = 0
        self.generate_priorities()

    def generate_priorities(self):
        pass
