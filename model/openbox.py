import numpy as np
import model.gacvm as gacvm
import model.umath as umath
import sys


class OpenBoxProblem:
    def __init__(self, width=10, height=5):
        self.__box_width = width
        self.__box_height = height
        self.__corner_range = np.array([[0, self.__box_height / 2]])
        self.__domains = gacvm.Domains(self.__corner_range, ('c',))

    @property
    def box_width(self):
        return self.__box_width

    @box_width.setter
    def box_width(self, value):
        self.__box_width = value

    @property
    def box_height(self):
        return self.__box_height

    @box_height.setter
    def box_height(self, value):
        self.__box_height = value

    @property
    def corner_range(self):
        return self.__corner_range

    @property
    def domains(self):
        return self.__domains

    def __call__(self, c):
        corner = c[0]
        return ((self.__box_height - (2 * corner)) * (self.__box_width - (2 * corner))) * corner


if __name__ == '__main__':
    open_box_problem = OpenBoxProblem(10, 5)
    new_problem = gacvm.ProblemDefinition(open_box_problem.domains, open_box_problem)

    genetic_algorithm = gacvm.GeneticAlgorithm(new_problem)
    genetic_algorithm.is_ready
    genetic_algorithm.evolve()
    genetic_algorithm.population
    pass
