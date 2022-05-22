import random
import numpy as np
import model.gacvm as gacvm
import model.umath as umath
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform
from __feature__ import snake_case, true_property

MIN_SATISFACTION = 0.00001

"""
Deux règles encadrent ce problème :
1. Il faut au moins 1 individu de chaque métier dans la population
2. Un métier ne peut être sureprésenté au-delà de 60%
La taille de la communauté spécifiée demeure une approximation.
L'algorithme effectue ses calculs dans l'ordre de grandeur spécifié.
"""


class HappyCommunityProblem:
    def __init__(self, community_context=None):
        self.__context = community_context
        self.__jobs_value = None
        self.__default_jobs = np.array([[3], [2], [2], [3]])
        self.__jobs_count = np.empty([1, 4])  # bracket supérieure = nbr de métiers
        self.generate_jobs_value()
        self.generate_domain()

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, community):
        self.__context = community

    @property
    def domains(self):
        return self.__domains

    def generate_jobs_value(self):
        """
        [0] -> Community Cost
        [1] -> Food Production
        [2] -> Goods Production
        [3] -> Health
        """
        self.__jobs_value = np.array(
            [[0.35, 0., 0., 0.8],  # Doctor
             [0.3, 0.1, 0.4, 0.125],  # Engineer
             [0.2, 0.7, 0., 0.05],  # Farmer
             [0.15, 0.1, 0.6, 0.025]],  # Worker
            dtype=float)

        self.__tags_jobs = np.array(
            ["Doctor", "Engineer", "Farmer", "Worker"]
            , dtype=np.str_
        )

    def generate_jobs_scores(self):
        return self.__jobs_count[:, :] * self.__jobs_value[:, :]

    def generate_sum_per_aspect(self):
        return np.sum(self.generate_jobs_scores(), axis=0)

    def generate_domain(self):
        self.__doctor_count = (1., self.context.community_size / 2)
        self.__engineer_count = (1., self.context.community_size / 2)
        self.__farmer_count = (1., self.context.community_size / 2)
        self.__worker_count = (1., self.context.community_size / 2)
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
        satisfaction = 0.

        self.__jobs_count = np.array([
            [jobs[0]],
            [jobs[1]],
            [jobs[2]],
            [jobs[3]],
        ])

        # On divise chaque résultat par la somme totale de population pour obtenir une proportion
        self.__jobs_count = np.around(self.__jobs_count[:, :] / np.sum(self.__jobs_count), 3)
        sum_per_aspect = self.generate_sum_per_aspect()
        aspects_weighted_scores = (sum_per_aspect[1:] * self.__context.weighted_aspects)
        if np.max(self.__jobs_count) > 0.6:
            satisfaction = MIN_SATISFACTION
        else:
            satisfaction = np.sum(aspects_weighted_scores) - sum_per_aspect[0]  # Soustraction par Community Cost
        return umath.clamp(MIN_SATISFACTION, satisfaction, satisfaction)

    # fonction utilitaire de formatage pour obtenir des valeurs relatives
    def format_solution(self, solution):
        return np.around(solution[:] / np.sum(solution), 3)


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
        self.__health = 0.
        self.__food_production = 0.
        self.__goods_production = 0.
        self.__weighted_aspects = None
        self.generate_priorities()  # Fonction qui génère la pondération des aspects de société

    @property
    def community_size(self):
        return self.__community_size

    @community_size.setter
    def community_size(self, size):
        self.__community_size = size

    @property
    def preset_contexts(self):
        return {
            "West, 2010-2019": np.array([0.275, 0.3, 0.425])
        }

    @property
    def weighted_aspects(self):
        return self.__weighted_aspects

    def set_weighted_aspects(self, aspects_array):
        self.__weighted_aspects = aspects_array

    # génère une pondération utilisée par la fitness function
    def generate_priorities(self):
        pass


# À SUPPRIMER AVANT REMISE, TEST SEULEMENT
if __name__ == '__main__':
    c = CommunityContext()
    c.set_weighted_aspects(c.preset_contexts["West, 2010-2019"])

    hcp = HappyCommunityProblem(c)
    # sum_per_aspect = hcp.generate_sum_per_aspect()
    # aspects_weighted_scores = (sum_per_aspect[1:] * c.weighted_aspects)
    # satisfaction_fitness_score = np.sum(aspects_weighted_scores) - sum_per_aspect[0]

    new_problem = gacvm.ProblemDefinition(hcp.domains, hcp)

    genetic_algorithm = gacvm.GeneticAlgorithm(new_problem)
    genetic_algorithm.evolve()

    best_solution = hcp.format_solution(genetic_algorithm.history.best_solution)

    pass

### RÉFÉRENCES ###

# Problème similaire : le 0-1 Knapsack
# https://medium.com/koderunners/genetic-algorithm-part-3-knapsack-problem-b59035ddd1d6
