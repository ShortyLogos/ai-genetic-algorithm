import numpy as np
import model.gacvm as gacvm
import model.umath as umath
import sys

def open_box_fitness(c):
    corner = c[0]
    return ((box_height - (2 * corner)) * (box_width - (2 * corner))) * corner

if __name__ == '__main__':
    # Construire une classe pour le OpenBoxProblem, avec self.__width et self.__height

    # Faire attention de ne pas faire des variables globales comme ceci dans le projet:
    # Dans la classe Qt du problème, les définir
    box_width = 10
    box_height = 5
    corner_range = np.array([[0, box_height / 2]])

    open_box_domains = gacvm.Domains(corner_range, ('c',))

    open_box_problem = gacvm.ProblemDefinition(open_box_domains, open_box_fitness)

    genetic_algorithm = gacvm.GeneticAlgorithm(open_box_problem)
    genetic_algorithm.is_ready
    genetic_algorithm.evolve()
    genetic_algorithm.population
    pass

    # ajout de vos stratégies
    # -------------------------------------------------------- par exemple
    # ga_app.add_crossover_strategy(my_awesome_strategy)
    # ga_app.add_mutation_strategy(ma_spectaculaire_strategie)
