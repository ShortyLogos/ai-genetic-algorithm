import numpy as np
import model.gacvm as gacvm
import model.umath as umath
import sys


def fitnessFunction(c):
    return ((box_height - (2 * c)) * (box_width - (2 * c))) * c

if __name__ == '__main__':
    box_width = 24.0
    box_height = 9.34

    cornerRange = np.array([[0, box_height / 2]])
    openBoxDomains = gacvm.Domains(cornerRange, ('c',))

    
    openBoxProblem = gacvm.ProblemDefinition(openBoxDomains, fitnessFunction(c))

    # ajout de vos stratégies
    # -------------------------------------------------------- par exemple
    # ga_app.add_crossover_strategy(my_awesome_strategy)
    # ga_app.add_mutation_strategy(ma_spectaculaire_strategie)
