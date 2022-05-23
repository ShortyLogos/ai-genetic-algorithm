######### Sommaire: Ce fichier contient une stratégie de mutation de gêne qu'on a inventé
######### Membres:
## Jean-Christophe Caron
## Samuel Horvath
## Déric Marchand
## Karl Robillard Marchand
######### Date de création:15/05/2022
from model.gacvm import MutationStrategy
import numpy as np

# ----------- WILD GENES MUTATION STRATEGY ----------------
# Permet d'appliquer une mutation sur plusieurs gènes à la fois.
# La probabilité d'affecter un gène donné diminue avec le nombre de gènes
# qui composent le chromosome.

# Ainsi, les entités plus complexes (chromosome étendu) subissent des changements moins
# prévisibles mais plus mesurés la plupart du temps, à l'image du monde naturel.
# Les entités plus simples sont quant à elles appelées à évoluer plus rapidement.

class WildGenesStrategy(MutationStrategy):
    def __init__(self):
        super().__init__()

    @staticmethod
    def name():
        return 'Wild Genes Strategy'

    def mutate(self, offsprings, mutation_rate, domains):
        def do_mutation(offspring, mutation_rate, domains):
            if self._rng.random() <= mutation_rate:
                for i in range(offsprings.shape[1]):
                    if self._rng.random() <= 1 / offsprings.shape[1]:
                        offspring[i] = domains.random_value(i)

        np.apply_along_axis(do_mutation, 1, offsprings, mutation_rate, domains)


