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

# Ce n'est pas un problème d'image, mais de géométrie!

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
        self.__surface = surface # QRectangleF
        self.__polygon = polygon # QPolygonF
        self.__obstacles_count = obstacles_count
        self.__translationX_range = (0., surface.width()) # -width à width du QRectangleF
        self.__translationY_range = (0., surface.height()) # -height à height du QRectangleF
        self.__rotation_range = (0., 360.)
        self.__scaling_range = (0., 5.) # Récupérer des valeurs de QRectangleF pour ce calcul ?
        self.__domains = gacvm.Domains(np.array([self.__translationX_range,
                                       self.__translationY_range,
                                       self.__rotation_range,
                                       self.__scaling_range], float),
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
            p.setX(p.x() + random.uniform(0, self.surface.width()))
            p.setY(p.y() + random.uniform(0, self.surface.height()))
            self.__obstacles.append(p)

    # fitness
    def __call__(self, dimensions):
        # corner = c[0]
        # return ((self.__box_height - (2 * corner)) * (self.__box_width - (2 * corner))) * corner
        self.transform.translate(dimensions[0], dimensions[1])
        self.transform.rotate(dimensions[2])
        self.transform.scale(dimensions[3], dimensions[3])
        # self.transform.map(self.polygon)
        # 1. transformation
        # 2. forme.checkPoints(point)
        # 3. canvas.intersects(forme)
        # IF 2 et 3 FALSE alors return AIRE
        # SINON return 0


class ShapeGenerator:
    def __init__(self, points_count, r=0, R=1):
        self.__min_points_count = 3
        self.__max_points_count = 32
        self.__r = r
        self.__R = R
        self.__points_count = 0
        self.points = points_count
        self.__shape = self.generate_shape()

    @property
    def points_count(self):
        return self.__points_count

    @points_count.setter
    def points_count(self, points_count):
        self.__points_count = umath.clamp(self.__min_points_count, points_count, self.__max_points_count)

    def generate_shape(self):
        shape = None
        if self.__points_count == 4:
            shape = QRectF(QPointF(-1, 1), QSize(1, 1))
        else:
            if self.__r == 0:
                self.generate_regular_polygon()
            else:
                GeometryOptimizationProblem.generate_concave_polygon(points_count, r, R)
        return shape

    def generate_regular_polygon(self):
        poly = QPolygonF()
        for i in range(self.__points_count):
            theta = i * ((2 * np.pi) / self.__points_count)
            x = np.cos(theta)
            y = np.sin(theta)
            poly.append(QPointF(x, y))
        return poly

    def generate_concave_polygon(points_count, r=0.5, R=1):
        poly = QPolygonF()
        for i in range(points_count):
            segment = ((2 * np.pi) / points_count)
            thetaR = i * segment
            thetar = thetaR + (0.5 * segment)

            xp = np.cos(thetaR) * R
            yp = np.sin(thetaR) * R
            poly.append(QPointF(xp, yp))

            xc = np.cos(thetar) * r
            yc = np.sin(thetar) * r
            poly.append(QPointF(xc, yc))
        return poly



# À SUPPRIMER AVANT REMISE, TEST SEULEMENT
if __name__ == '__main__':
    # CRÉATION DES OBJETS QT
    surface = QRectF()

    # Valeurs imposées à titre pratique
    # comme dans l'exemple du professeur
    surface.setWidth(500)
    surface.setHeight(250)

    geometry_optimization_problem = GeometryOptimizationProblem(surface, 5, 5)
    new_problem = gacvm.ProblemDefinition(geometry_optimization_problem.domains, geometry_optimization_problem)

    genetic_algorithm = gacvm.GeneticAlgorithm(new_problem)
    # genetic_algorithm.is_ready
    # genetic_algorithm.evolve()
    # genetic_algorithm.population

    print(GeometryOptimizationProblem.generate_regular_polygon(3))