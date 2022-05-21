from gacvm import MutationStrategy
import numpy as np

# pour appliquer la stratégie :
# une instance de ga a une variable parameters, qui est un objet
# ex : ga.parameters pour obtenir l'instance
# ga.instance_de_parameters.mutation_strategy = instance_strategie_mutation_personnalisee
# instance_de_parameters.mutation_strategy = instance_strategie_mutation_personnalisee

class BustScalingLimitStrategy(MutationStrategy):
    def __init__(self):
        super().__init__()

    @staticmethod
    def name():
        return 'Bust Natural Scaling Limit'

    def mutate(self, offsprings, mutation_rate, domains):
        def do_mutation(offspring, mutation_rate, domains):
            if self._rng.random() <= mutation_rate:
                # index = self._rng.integers(0, offspring.shape[1]) # de 0 au nbr de domaine de l'enfant
                offspring[3] = domains.random_value(3) + domains.random_value(3)

        np.apply_along_axis(do_mutation, 1, offsprings, mutation_rate, domains)

