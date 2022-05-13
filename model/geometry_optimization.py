import numpy as np
import model.gacvm as gacvm
import model.umath as umath
import sys

# Quelle est la transformation?

# Problème à 4 dimensions :
# 1. TranslationX
# 2. TranslationY
# 3. Rotation (1 paramètre puisque en 2D)
# 4. Homothétie (scaling) (Égale en X et en Y pour conserver la forme)

# On a pas un problème d'image.
# Un problème de géométrie.

# On a trois primitives géométriques : rectangle (canevas), liste de points (obstacles), polygone (shape à faire fitter)
# Est-ce que ce polygone est à l'intersection d'un obstacle ?
# Pas de numpy à tour de bras.
# Qt -> On utilise des librairies

# Il faudra le présenter à l'écran. Faire le lien entre ce qu'on et ce qu'on a de besoin.
# Matrices de transformation : changement de référentiel
# Tout ce qui se passe dans la carte vidéo sert avant tout à faire le calcul matriciel
# QTransform.map -> On y passe notre polygone et ça nous retourne un nouveau polygone transformé et c'est lui qu'on utilise
# UQTGui pour aire et périmètre du polygone

# Référentiel -> Centre de la forme
# Forme normalisée -> 0 à 1 de chaque côté

class GeometryOptimizationProblem:
    def __init__(self, polygon, obstacles):
        self.__polygon = polygon
        self.__obstacles = obstacles
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