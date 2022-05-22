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
        self.__jobs_value = None
        self.generate_jobs()
        self.__priorities = None  # array des coefficients de pondération selon le contexte
        # méthode generate_priorities(community_context) ?
        self.generate_domain()
        self.__domains = gacvm.Domains(np.array([
            0
        ], float),
            ('doctor', 'engineer', 'farmer', 'worker'))

    @property
    def community_context(self):
        return self.__community_context

    @community_context.setter
    def community_context(self, new_community):
        self.__community_context = new_community

    def generate_jobs(self):
        """
        [0] -> Community Cost,
        [1] -> Food Production,
        [2] -> Goods Production,
        [3] -> Health
        """
        self.__jobs_value = np.array(
            [[0.5], [0.], [0.], [0.8]],  # Doctor
            [[0.375], [0.15], [0.35], [0.125]],  # Engineer
            [[0.1], [0.6], [0.], [0.05]],  # Farmer
            [[0.025], [0.25], [0.65], [0.025]],  # Worker
            dtype=float)

    def generate_domain(self):

    def __call__(self, jobs):
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
        self.__religious_sentiment = 10
        self.__domestic_stability = 10
        self.__education_rate = 1
        # Ci-dessous, les priorités d'une communauté (moyenne pondérée dont la somme = 1)
        self.__community_cost = 0
        self.__health = 0
        self.__food_production = 0
        self.__goods_production = 0
        self.generate_priorities()

    def generate_priorities(self):
        pass
