import random
import numpy as np
import model.gacvm as gacvm
import model.umath as umath
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform
from __feature__ import snake_case, true_property


class HappyCommunityProblem:
    def __init__(self, community_context=None):
        self.__context = community_context
        # self.__preset_contexts = np.array()
        self.__jobs_value = None
        self.generate_jobs_value()
        self.generate_domain()

    @property
    def context(self):
        return self.__community_context

    @context.setter
    def context(self, community):
        self.__community_context =community

    def generate_jobs_value(self):
        """
        [0] -> Community Cost
        [1] -> Food Production
        [2] -> Goods Production
        [3] -> Health
        """
        self.__jobs_value = np.array(
            [[0.5], [0.], [0.], [0.8]],  # Doctor
            [[0.375], [0.15], [0.35], [0.125]],  # Engineer
            [[0.1], [0.6], [0.], [0.05]],  # Farmer
            [[0.025], [0.25], [0.65], [0.025]],  # Worker
            dtype=float)

    def generate_domain(self):
        self.__doctor_count = (0., self.context.community_size)
        self.__engineer_count = (0., self.context.community_size)
        self.__farmer_count = (0., self.context.community_size)
        self.__worker_count = (0., self.context.community_size)
        self.__domains = gacvm.Domains(np.array([
            self.__doctor_count,
            self.__engineer_count,
            self.__farmer_count,
            self.__worker_count
        ], float),
            ('doctor', 'engineer', 'farmer', 'worker'))

    def __call__(self, jobs):
        """
        calcul de l'indice de satisfaction :
        1. Calcul de la somme pondérée de chaque aspect:
            - Multiplication du nombre de jobs * valeur de l'aspect concerné par scalaire
            - Somme de ces résultats * pondération
        2. Somme du résultat pondéré de chaque aspect - score du coût de communauté (community cost)
        somme de tous les scores pondérés des différents aspects de société
        """
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
    """
    On doit faire appel à des setters pour les paramétrer
    """
    def __init__(self, socio_political_context=None, community_size=200):
        self.__socio_political_context = socio_political_context
        self.__community_size = float(community_size)

        # Traits de personnalité d'une communauté
        self.__religious_sentiment = 3.
        self.__domestic_stability = 3.5
        self.__education_rate = 3.8

        # Ci-dessous, les priorités d'une communauté (moyenne pondérée dont la somme = 1)
        # self.__community_cost = ... la pondération du CC est toujours de 1
        self.__health = 4.
        self.__food_production = 4.
        self.__goods_production = 4.
        self.generate_priorities()

    @property
    def community_size(self):
        return self.__community_size

    @community_size.setter
    def community_size(self, size):
        self.__community_size = size

    # génère une pondération utilisée par la fitness function
    def generate_priorities(self):
        pass
