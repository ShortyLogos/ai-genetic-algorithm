######### Sommaire: Ce fichier contient l'algorithme génétique relié au problème trois pour etre instancié dans community_vue
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:20/05/2022
### RÉFÉRENCES ###
# Problème similaire : le 0-1 Knapsack
# https://medium.com/koderunners/genetic-algorithm-part-3-knapsack-problem-b59035ddd1d6
import random
import numpy as np
import model.gacvm as gacvm
import model.umath as umath
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform
from __feature__ import snake_case, true_property

### RÉFÉRENCES ###

# Problème similaire : le 0-1 Knapsack
# https://medium.com/koderunners/genetic-algorithm-part-3-knapsack-problem-b59035ddd1d6

"""
UNE RÈGLE ENCADRE LE « HAPPY COMMUNITY PROBLEM » :
Il faut au moins 1 individu de chaque métier dans la population afin d'empêcher les divisions par zéro

La taille de la communauté spécifiée demeure une approximation.
L'algorithme effectue ses calculs dans l'ordre de grandeur spécifié,
mais il est théoriquement possible d'obtenir pour une solution des valeurs extrêmement
éloignées de la taille de la communauté spécifiée.
"""

"""
Structure des tableaux numpy liés aux aspects de société:
[0] -> Community Cost
[1] -> Food Production
[2] -> Goods Production
[3] -> Health
[4] -> Culture
[5] -> Entertainement
[6] -> Spirituality
[7] -> Stability
[8] -> Public Hyigene
"""
ASPECTS_MODEL = np.empty([9])
MIN_SATISFACTION = 0.0001


class HappyCommunityProblem:
    def __init__(self, community_context=None):
        self.__context = community_context
        self.__jobs_value = None
        self.__default_jobs = np.array([[3], [2], [2], [3]])
        self.__jobs_count = np.empty([1, 4])  # bracket supérieure = nbr de métiers
        self.__max_single_job = 0.6
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

    @property
    def max_single_job(self):
        return self.__max_single_job

    @max_single_job.setter
    def max_single_job(self, val):
        self.__max_single_job = umath.clamp(0, val, 1)

    @property
    def jobs_tags(self):
        return np.array(
            ["Doctor", "Engineer", "Farmer", "Worker", "Artist", "Customer Service",
             "Dentist", "Garbage Collector", "Spiritual Enforcer", "Laywer", "Nurse",
             "Politician", "Teacher", "Police", "Military", "Therapist"]
            , dtype=np.str_)

    def generate_jobs_value(self):
        self.__jobs_value = np.array(
            [[0.5, 0., 0., 0.775],  # Doctor
             [0.3, 0.25, 0.4, 0.1475],  # Engineer
             [0.065, 0.55, 0.025, 0.0075],  # Farmer
             [0.05, 0.1, 0.575, 0.07]],  # Worker
            dtype=float)

    def generate_jobs_scores(self):
        # return self.__jobs_count[:, :] * self.__jobs_value[:, :]

        # avec JC
        # resulted_value = self.__jobs_value[:, :]
        # resulted_value[:, 1:] = self.__jobs_count[:, :] * resulted_value[:, :]
        # # pass
        # # resulted_value[:, 0] = resulted_value[:, 0] ** (1/self.__jobs_count[0, :])
        # return resulted_value

        resulted_value = self.__jobs_value.copy()
        resulted_value[:, 1:] = self.__jobs_count[:, :] * self.__jobs_value[:, 1:]
        resulted_value[:, 0] = self.__jobs_value[:, 0] ** (1/self.__jobs_count[:, 0])
        return resulted_value

    def generate_sum_per_aspect(self):
        return np.sum(self.generate_jobs_scores(), axis=0)

    def generate_domain(self):
        self.__doctor_count = (1., self.context.community_size)
        self.__engineer_count = (1., self.context.community_size)
        self.__farmer_count = (1., self.context.community_size)
        self.__worker_count = (1., self.context.community_size)
        self.__domains = gacvm.Domains(np.array([
            self.__doctor_count,
            self.__engineer_count,
            self.__farmer_count,
            self.__worker_count
        ], float),
            ('doctor', 'engineer', 'farmer', 'worker'))

    def __call__(self, jobs):
        """
        Calcul de l'indice de satisfaction :
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
        satisfaction = np.sum(aspects_weighted_scores) - (sum_per_aspect[0] * self.context.uncertainty)  # Soustraction par Community Cost
        satisfaction = umath.clamp(MIN_SATISFACTION, satisfaction, satisfaction)
        return satisfaction

    # fonction utilitaire de formatage pour obtenir des valeurs relatives
    def format_solution(self, solution):
        return np.around(solution[:] / np.sum(solution), 3)


class SocioPoliticalContext:
    def __init__(self, life_expectancy=60):
        self.__life_expectancy = life_expectancy
        self.__life_expectancy_min = 15
        self.__life_expectancy_max = 110
        self.__aspects_influence = np.zeros([3], dtype=float)
        self.__events = {
            "Cultural Shift": False,
            "Economic Crisis": False,
            "Political Instability": False,
            "War Raging": False,
            "Global Warming": False,
            "Epidemic": False
        }
        self.generate_influence()


    def generate_influence(self):
        """
        """
        pass

    @property
    def events(self):
        return self.__events

    def set_event(self, key, bool):
        self.__events[key] = bool

    @property
    def life_expectancy(self):
        return self.__life_expectancy

    @life_expectancy.setter
    def life_expectancy(self, val):
        self.__life_expectancy = val

    @property
    def life_expectancy_min(self):
        return self.__life_expectancy_min

    @property
    def life_expectancy_max(self):
        return self.__life_expectancy_max


class CommunityContext:
    """
    On doit faire appel à des setters pour les paramétrer
    """

    def __init__(self, socio_political_context=None, community_size=200):
        self.__socio_political_context = socio_political_context
        self.__community_size = float(community_size)
        self.__community_min_size = 50
        self.__community_max_size = 100000
        self.__uncertainty = 1  # de 0 à 2, 2 représentant l'incertitude maximale, 0.5 la liesse des années folles

        # Traits de personnalité d'une communauté
        self.__min_trait_value = 1.
        self.__max_trait_value = 10.
        self.__community_traits = {
            "Religious Sentiment": 3.,
            "Domestic Stability": 3.,
            "Education Rate": 3.
        }

        # Ci-dessous, les priorités d'une communauté (moyenne pondérée dont la somme = 1)
        # self.__community_cost = ... la pondération du CC est toujours de 1
        self.__health = 1.
        self.__food_production = 1.
        self.__goods_production = 1.
        self.__aspects = None
        self.__weighted_aspects = None
        self.generate_priorities()  # Fonction qui génère la pondération des aspects de société

        [3, 2, 5.5,]
        [+1, -0.2, +3, ...]

        [4, 1.8, 3, 49]


    @property
    def socio_political_context(self):
        return self.__socio_political_context

    @socio_political_context.setter
    def socio_political_context(self, sp_context):
        self.__socio_political_context = sp_context

    @property
    def community_size(self):
        return self.__community_size

    @community_size.setter
    def community_size(self, size):
        self.__community_size = size

    @property
    def community_min_size(self):
        return self.__community_min_size

    @property
    def community_max_size(self):
        return self.__community_max_size

    @community_max_size.setter
    def community_max_size(self, val):
        self.__community_max_size = val

    @property
    def community_traits(self):
        return self.__community_traits

    def set_community_trait(self, key, val):
        self.__community_traits[key] = umath.clamp(self.__min_trait_value, val, self.__max_trait_value)

    @property
    def min_trait_value(self):
        return self.__min_trait_value

    @property
    def max_trait_value(self):
        return self.__max_trait_value

    @property
    def uncertainty(self):
        return self.__uncertainty

    @property
    def weighted_aspects(self):
        return self.__weighted_aspects

    @property
    def preset_contexts(self):
        return {
            "West, 2010-2019": np.array([0.335, 0.3, 0.365])
        }

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
    print(genetic_algorithm.history.best_fitness)
    print(genetic_algorithm.history.best_solution)
    print(best_solution)
    pass