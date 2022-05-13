import random

import numpy as np
import model.gacvm as gacvm
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform
from PySide6 import *
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
    def __init__(self, surface, polygon, obstacles_count):
        self.__polygon = polygon # QPolygonF
        self.__surface = surface # QRectangleF
        self.__obstacles_count = obstacles_count
        self.__translationX_range = np.array([-500, 500]) # -width à width du QRectangleF
        self.__translationY_range = np.array([-500, 500]) # -height à height du QRectangleF
        self.__rotation_range = np.array([0, 360])
        self.__scaling_range = np.scale([0, 5]) # Récupérer des valeurs de QRectangleF pour ce calcul ?
        self.__domains = gacvm.Domains(np.array([self.__translationX_range],
                                       [self.__translationY_range],
                                       [self.__rotation_range],
                                       [self.__scaling_range]),
                                       ('tx', 'ty', 'r', 's'))
        self.__obstacles = []
        self.transform = QTransform()
        self.generate_obstacles()


    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, new_surface):
        self.__surface = new_surface

    @property
    def polygon(self):
        return self.__polygon

    @polygon.setter
    def polygon(self, new_polygon):
        self.__polygon = new_polygon

    @property
    def obstacles_count(self):
        return self.__obstacles_count

    @obstacles_count.setter
    def obstacles_count(self, value):
        self.__obstacles_count = value

    @property
    def domains(self):
        return self.__domains

    def generate_obstacles(self):
        self.__obstacles.clear()
        for _ in range(self.__obstacles_count):
            p = QPointF()
            p.setX(p.x() + random.uniform(0, self.surface.width))
            p.setY(p.y() + random.uniform(0, self.surface.height))
            self.__obstacles.append(p)

    # fitness
    def __call__(self, dimensions):
        # corner = c[0]
        # return ((self.__box_height - (2 * corner)) * (self.__box_width - (2 * corner))) * corner
        self.transform.translate(dimensions[0], dimensions[1])
        self.transform.rotate(dimensions[2])
        self.transform.scale(dimensions[3], dimensions[3])
        self.transform.map(self.polygon)
        # 1. transformation
        # 2. forme.checkPoints(point)
        # 3. canvas.intersects(forme)
        # IF 2 et 3 FALSE alors return AIRE
        # SINON return 0


if __name__ == '__main__':
    open_box_problem = GeometryOptimizationProblem()
    new_problem = gacvm.ProblemDefinition(open_box_problem.domains, open_box_problem)

    genetic_algorithm = gacvm.GeneticAlgorithm(new_problem)
    genetic_algorithm.is_ready
    genetic_algorithm.evolve()
    genetic_algorithm.population
    pass