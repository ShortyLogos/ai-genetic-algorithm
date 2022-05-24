######### Sommaire: Problème no. 3 avec destiné à être instancié dans community_vue
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
MIN_SATISFACTION = 0.0001


class SocioPoliticalContext:
    def __init__(self, life_expectancy=60):
        self.__life_expectancy = life_expectancy
        self.__life_expectancy_min = 15
        self.__life_expectancy_max = 110
        self.__aspects_influence = np.zeros([3], dtype=float)
        self.__uncertainty = 1
        self.__influence = np.array([.0, .0, .0, .0, .0, .0, .0, .0, .0]) # le dernier indice influence le degré d'incertitude
        self.__events = {
            "Cultural Shift": False,
            "Economic Crisis": False,
            "Political Instability": False,
            "War Raging": False,
            "Global Warming": False,
            "Epidemic": False
        }
        self.__events_values = {
            "Cultural Shift": np.array([0, 0, 0, .3, .2, .1, -.2,  -0.35, -.05]),
            "Economic Crisis": np.array([0, -.2, -.1, -.1, -.2, -.025, .1, 0, .1]),
            "Political Instability": np.array([0, 0, -.05, -.1, -.2, -.1, .2, -.1, .125]),
            "War Raging": np.array([0, .15, -.05, -.5, -.2, .015, .135, .15, .4]),
            "Global Warming": np.array([.1, -.1, 0, 0, -.1, .005, .05, 0, .15]),
            "Epidemic": np.array([.1, -.3, .2, -.1, -.3, .1, .2, -0.05, .2])
        }

    def generate_influence(self):
        self.generate_events()
        self.life_expectancy_impact()
        self.__uncertainty += self.__influence[-1]

    def generate_events(self):
        events = self.__events.keys()
        for key in events:
            if self.__events[key]:
                self.__influence += self.__events_values[key]
        return self.__influence

    def life_expectancy_impact(self):
        if self.__life_expectancy < 20:
            self.__influence += np.array([.1, -.2, -.07, -.2, -.2, .2, .175, -.1, .4])
        elif self.__life_expectancy < 30:
            self.__influence += np.array([.07, -.1, -.05, -.1, -.1, .1, .1, -.1, .25])
        elif self.__life_expectancy < 40:
            self.__influence += np.array([.05, -.035, -.05, .0, -.1, .1, -.2, -.05, .08])
        elif self.__life_expectancy < 50:
            self.__influence += np.array([.04, .0, -.05, .0, .05, .05, 0, -.02, .02])
        elif self.__life_expectancy < 60:
            self.__influence += np.array([.0, .025, .015, .025, .055, .0, 0, 0, 0])
        elif self.__life_expectancy < 70:
            self.__influence += np.array([.01, .035, 0, .07, .06, .025, .0, .025, -.005])
        elif self.__life_expectancy < 80:
            self.__influence += np.array([.02, .04, 0, .08, .075, .05, -.05, .05, -.015])
        elif self.__life_expectancy < 90:
            self.__influence += np.array([.03, .05, .05, .1, .095, .08, -.075, .08, -.05])
        else:
            self.__influence += np.array([.04, .06, .1, .15, .1, .15, -.1, .1, -.1])

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

    @property
    def influence(self):
        return self.__influence

    @property
    def uncertainty(self):
        return self.__uncertainty

    def uncertainty_change(self, val):
        self.__uncertainty += val


class CommunityContext:
    """
    On doit faire appel à des setters pour paramétrer les traits de la communauté.
    Indices auxquels font référence les fonctions de calculs de traits:

    [0] -> Food Production
    [1] -> Goods Production
    [2] -> Health
    [3] -> Culture
    [4] -> Entertainement
    [5] -> Spirituality
    [6] -> Stability
    [7] -> Public Hyigene
    """

    def __init__(self, socio_political_context=SocioPoliticalContext(), community_size=500):
        self.__socio_political_context = socio_political_context
        self.__community_size = float(community_size)
        self.__community_min_size = 50
        self.__community_max_size = 1000000

        # Traits de personnalité d'une communauté
        self.__default_trait_value = 4.
        self.__min_trait_value = 1.
        self.__max_trait_value = 10.
        self.__community_traits = {
            "Religious Sentiment": self.__default_trait_value,
            "Domestic Stability": self.__default_trait_value,
            "Education Rate": self.__default_trait_value
        }

        # Ci-dessous, les priorités d'une communauté (moyenne pondérée dont la somme = 1)
        self.__aspects = np.ones([8], dtype=float) # nbr d'aspects excluant le Community Cost
        self.__weighted_aspects = None
        self.generate_priorities()  # Fonction qui génère la pondération des aspects de société

    # génère une pondération utilisée par la fitness function
    def generate_priorities(self):
        self.__socio_political_context.generate_influence()
        self.__aspects += self.__socio_political_context.influence[:-1]
        self.__community_size_impact()
        self.__religious_sentiment_impact()
        self.__domestic_stability_impact()
        self.__education_rate_impact()
        self.__weighted_aspects = np.around(self.__aspects[:] / np.sum(self.__aspects), 3)

    def __community_size_impact(self):
        self.__aspects[0] += self.__community_size / 100000
        self.__aspects[1] += self.__community_size / 85000
        self.__aspects[2] += self.__community_size / 70000
        self.__aspects[4] += self.__community_size / 80000
        self.__aspects[6] += self.__community_size / 60000
        self.__aspects[7] += self.__community_size / 85000
        self.__socio_political_context.uncertainty_change(self.__community_size / 150000)

    def __religious_sentiment_impact(self):
        if self.__community_traits["Religious Sentiment"] < 5:
            self.__aspects[1] += 1. - (self.__community_traits["Religious Sentiment"] / 100)
            self.__aspects[4] += 1. - (self.__community_traits["Religious Sentiment"] / 125)
            self.__aspects[5] -= 1. - (self.__community_traits["Religious Sentiment"] / 100)
        else:
            self.__aspects[4] -= self.__community_traits["Religious Sentiment"] / 150
            self.__aspects[5] += self.__community_traits["Religious Sentiment"] / 100
            self.__aspects[6] += self.__community_traits["Religious Sentiment"] / 150
        self.__aspects[0] += self.__community_traits["Religious Sentiment"] / 185
        self.__aspects[3] += self.__community_traits["Religious Sentiment"] / 200

    def __domestic_stability_impact(self):
        self.__aspects[0] += self.__community_traits["Domestic Stability"] / 150
        self.__aspects[0] += self.__community_traits["Domestic Stability"] / 90
        self.__aspects[4] += self.__community_traits["Domestic Stability"] / 150
        self.__aspects[5] += self.__community_traits["Domestic Stability"] / 150
        self.__aspects[6] += self.__community_traits["Domestic Stability"] / 210
        self.__aspects[7] += self.__community_traits["Domestic Stability"] / 125

    def __education_rate_impact(self):
        self.__aspects[1] -= self.__community_traits["Education Rate"] / 135
        self.__aspects[2] += self.__community_traits["Education Rate"] / 125
        self.__aspects[3] += self.__community_traits["Education Rate"] / 100
        self.__aspects[4] -= self.__community_traits["Education Rate"] / 140
        self.__aspects[5] -= self.__community_traits["Education Rate"] / 90
        self.__aspects[6] -= self.__community_traits["Education Rate"] / 90
        self.__aspects[7] -= self.__community_traits["Education Rate"] / 85

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
    def default_trait_value(self):
        return self.__default_trait_value

    @property
    def min_trait_value(self):
        return self.__min_trait_value

    @property
    def max_trait_value(self):
        return self.__max_trait_value

    @property
    def weighted_aspects(self):
        return self.__weighted_aspects

    @property
    def preset_gui_contexts(self):
        return {
            "Neutral": [60, 5, 5, 5, False, False, False, False, False, False],
            "Mushroom Haircut Era": [100, 1, 10, 1, True, False, True, False, True, False],
            "Fall of the Roman Empire": [40, 7, 4, 4, True, True, True, True, False, False],
            "2020": [80, 6, 6, 6, False, True, False, False, True, True]
        }

    def set_weighted_aspects(self, aspects_array):
        self.__weighted_aspects = aspects_array


class HappyCommunityProblem:
    def __init__(self, community_context=CommunityContext()):
        self.__context = community_context
        self.__domains = None
        self.__jobs_value = None
        self.__jobs_count = np.empty([1, 16])  # bracket supérieure = nbr de métiers
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
    def jobs_tags(self):
        return np.array(
            ["Doctor", "Engineer", "Farmer", "Worker", "Artist", "Customer Service",
             "Dentist", "Garbage Collector", "Spiritual Leader", "Lawyer", "Nurse",
             "Politician", "Teacher", "Emergency", "Athlete", "Therapist"]
            , dtype=np.str_)

    @property
    def aspects_tags(self):
        return np.array(
            ["Communtiy Cost", "Food Production", "Goods Production", "Health",
             "Culture", "Entertainement", "Spirituality", "Stability", "Public Hygiene"]
            , dtype=np.str_)

    def generate_jobs_value(self):
        self.__jobs_value = np.array(
            [[0.10625,      0.05,   0.,     0.6,    0.,     0.,     0.,     0.075,  0.1],   # Doctor
             [0.0775,       0.15,   0.2,    0.07,   0.05,   0.1,    0.,     0.05,   0.05],  # Engineer
             [0.075625,     0.6,    0.,     0.005,  0.,     0.,     0.,     0.,     0.],    # Farmer
             [0.084375,     0.15,   0.5,    0.,     0.,     0.025,  0.,     0.,     0.],    # Worker
             [0.1125,       0.,     0.05,   0.05,   0.35,   0.45,   0.05,   0.,     0.],    # Artist
             [0.0375,       0.05,   0.1,    0.0015, 0.,     0.,     0.05,   0.,     0.1],   # Customer Service
             [0.035625,     0.,     0.,     0.07,   0.,     0.,     0.,     0.025,  0.215], # Dentist
             [0.05625,      0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.4],   # Garbage Collector
             [0.075,        0.,     0.,     0.,     0.,     0.05,   0.55,   0.005,  0.],    # Spiritual Leader
             [0.034375,     0.,     0.05,   0.,     0.05,   0.,     0.,     0.12,   0.],    # Lawyer
             [0.015,        0.,     0.,     0.12,   0.,     0.,     0.,     0.,     0.05],  # Nurse
             [0.0375,       0.,     0.1,    0.,     0.15,   0.,     0.,     0.05,   0.],    # Politician
             [0.05,         0.,     0.,     0.,     0.25,   0.1,    0.,     0.,     0.05],  # Teacher
             [0.0721875,    0.,     0.,     0.0225, 0.,     0.,     0.,     0.475,  0.],    # Emergency
             [0.06,         0.,     0.,     0.0035, 0.15,   0.225,  0.1,    0.,     0.],    # Athlete
             [0.0703125,    0.,     0.,     0.1075, 0.,     0.,     0.3,    0.1,    0.055]  # Therapist
             ],
            dtype=float)

    def generate_jobs_scores(self):
        resulted_value = self.__jobs_value.copy()
        resulted_value[:, 1:] = self.__jobs_count[:, :] * self.__jobs_value[:, 1:]
        resulted_value[:, 0] = self.__jobs_value[:, 0] ** (1 / self.__jobs_count[:, 0])
        # resulted_value[:, 0] += self.__jobs_count[:, 0] * self.__jobs_value[:, 0]
        return resulted_value

    def generate_sum_per_aspect(self):
        return np.sum(self.generate_jobs_scores(), axis=0)

    def generate_domain(self):
        jobs = np.tile(np.array((self.context.community_size * 0.005, self.context.community_size)), (16, 1))
        self.__domains = gacvm.Domains(jobs,
            ('doctor', 'engineer', 'farmer', 'worker', 'artist', 'customer_service', 'dentist', 'garbage_collector',
             'spiritual_leader', 'lawyer', 'nurse', 'politician', 'teacher', 'emergency', 'athlete', 'therapist'))

    def __call__(self, jobs):
        """
        Calcul de l'indice de satisfaction :
        1. Calcul de la somme pondérée de chaque aspect:
            - Multiplication du nombre de jobs * valeur de l'aspect concerné par scalaire
            - Somme de ces résultats * pondération
        2. Somme du résultat pondéré de chaque aspect - score du coût de communauté (community cost)
            multiplié par la taille de la communauté et le facteur d'incertitude
        """

        self.__jobs_count = np.array([
            [jobs[0]],
            [jobs[1]],
            [jobs[2]],
            [jobs[3]],
            [jobs[4]],
            [jobs[5]],
            [jobs[6]],
            [jobs[7]],
            [jobs[8]],
            [jobs[9]],
            [jobs[10]],
            [jobs[11]],
            [jobs[12]],
            [jobs[13]],
            [jobs[14]],
            [jobs[15]]
        ])

        # On divise chaque résultat par la somme totale de population pour obtenir une proportion
        self.__jobs_count = np.around(self.__jobs_count[:, :] / np.sum(self.__jobs_count), 3)
        sum_per_aspect = self.generate_sum_per_aspect()
        aspects_weighted_scores = (sum_per_aspect[1:] * self.__context.weighted_aspects)
        satisfaction = np.sum(aspects_weighted_scores) - (sum_per_aspect[0] * self.context.socio_political_context.uncertainty)  # Soustraction du Community Cost à l'indice de satisfaction
        return umath.clamp(MIN_SATISFACTION, satisfaction, satisfaction)

    # fonction utilitaire de formatage pour obtenir des valeurs relatives
    def format_solution(self, solution):
        return np.around(solution[:] / np.sum(solution), 3)


# À SUPPRIMER AVANT REMISE, TEST SEULEMENT
if __name__ == '__main__':
    hcp = HappyCommunityProblem()
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
