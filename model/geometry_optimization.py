import random
import numpy as np
import model.gacvm as gacvm
import model.umath as umath
from PySide6.QtCore import Qt, Slot, Signal, QSize, QPointF, QRectF
from PySide6.QtGui import QPolygonF, QTransform

from __feature__ import snake_case, true_property

### RÉFÉRENCES ###

# Calcul de l'aire d'un QPolygonF
# https://stackoverflow.com/questions/67558984/how-calculate-qpolygon-area


class GeometryOptimizationProblem:

    def __init__(self, surface_width=500, surface_height=250, obstacles_count=0, min_obstacles=1):
        self.__surface = QRectF(0, 0, surface_width, surface_height)
        self.__polygon = None
        self.__obstacles = []
        self.__min_obstacles = min_obstacles
        self.__max_obstacles = 0
        self.calculate_max_obstacles()
        if obstacles_count == 0:
            self.__obstacles_count = int(self.__max_obstacles / 2)
        else:
            self.__obstacles_count = obstacles_count
        self.generate_obstacles()
        self.generate_domain()

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, new_surface):
        self.__surface = new_surface
        self.calculate_max_obstacles()
        self.generate_domain()

    @property
    def obstacles(self):
        return self.__obstacles

    @property
    def min_obstacles(self):
        return self.__min_obstacles

    @property
    def max_obstacles(self):
        return self.__max_obstacles

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
        self.__obstacles_count = umath.clamp(1, value, self.__max_obstacles)

    @property
    def domains(self):
        return self.__domains

    def generate_domain(self):
        self.__translationX_range = (0., self.__surface.width())
        self.__translationY_range = (0., self.__surface.height())
        self.__rotation_range = (0., 360.)
        self.__scaling_range = (0., self.scaling_upper_bracket(self.__surface.width(), self.__surface.height()))
        self.__domains = gacvm.Domains(np.array([self.__translationX_range,
                                                 self.__translationY_range,
                                                 self.__rotation_range,
                                                 self.__scaling_range], float),
                                       ('tx', 'ty', 'r', 's'))

    def scaling_upper_bracket(self, surface_width, surface_height):
        return float(max(surface_width, surface_height) / 2)

    def calculate_max_obstacles(self, max_covered_ratio=0.8):
        self.__max_obstacles = int(max(self.__surface.width(), self.__surface.height()) * max_covered_ratio)

    def generate_obstacles(self):
        self.__obstacles.clear()
        for _ in range(self.__obstacles_count):
            p = QPointF()
            p.set_x(p.x() + random.uniform(0, self.surface.width()))
            p.set_y(p.y() + random.uniform(0, self.surface.height()))
            self.__obstacles.append(p)

    def calculate_area(self, poly):
        poly_area = 0.
        for i in range(poly.size()):
            p1 = poly[i]
            p2 = poly[(i + 1) % poly.size()]
            d = p1.x() * p2.y() - p2.x() * p1.y()
            poly_area += d
        return abs(poly_area) / 2

    # fitness function
    def __call__(self, dimensions):
        t = QTransform()
        t.translate(dimensions[0], dimensions[1])
        t.rotate(dimensions[2])
        t.scale(dimensions[3], dimensions[3])
        modified_poly = t.map(self.__polygon)
        for obstacle in self.__obstacles:
            if modified_poly.contains_point(obstacle, Qt.OddEvenFill):
                return 0.
        for vertex in modified_poly:
            if self.__surface.contains(vertex) is False:
                return 0.
        return self.calculate_area(modified_poly)


class ShapeGenerator:
    def __init__(self, vertex_count=3, r=0, R=1):
        self.__shape = None
        self.__vertex_count = 0
        self.__min_vertex_count = 3
        self.__max_vertex_count = 32
        self.__min_concavity = 0
        self.__max_concavity = 1
        self.__r = r
        self.__R = R
        self.vertex_count = vertex_count
        self.__poly_angle = self.__vertex_count * ((2 * np.pi) / self.__vertex_count)
        self.generate_shape()

    @property
    def preset_shapes(self):
        return {"Triangle": [3, 0],
                "Square": [4, 0],
                "Star 5": [5, 0.5]}

    @property
    def shape(self):
        return self.__shape

    @property
    def vertex_count(self):
        return self.__vertex_count

    @property
    def min_vertex_count(self):
        return self.__min_vertex_count

    @property
    def max_vertex_count(self):
        return self.__max_vertex_count

    @property
    def min_concavity(self):
        return self.__min_concavity

    @property
    def max_concavity(self):
        return self.__max_concavity

    @vertex_count.setter
    def vertex_count(self, vertex_count):
        self.__vertex_count = umath.clamp(self.__min_vertex_count, vertex_count, self.__max_vertex_count)

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, val):
        self.__r = umath.clamp(self.__min_concavity, val, self.__max_concavity)

    def generate_shape(self):
        self.__shape = QPolygonF()
        self.generate_regular_polygon() if self.__r == 0 else self.generate_concave_polygon()

    def generate_regular_polygon(self):
        self.__shape.resize(self.__vertex_count)
        for i in range(self.__vertex_count):
            theta = i * ((2 * np.pi) / self.__vertex_count)
            x = np.cos(theta)
            y = np.sin(theta)
            self.__shape[i] = QPointF(x, y)

    def generate_concave_polygon(self):
        self.__shape.resize(self.__vertex_count * 2)
        segmentation = ((2 * np.pi) / self.__vertex_count)
        for i in range(self.__vertex_count):
            thetaR = i * segmentation
            # nextTheta = (i + 1) * segmentation
            thetar = (i + 0.5) * segmentation

            xp = np.cos(thetaR)
            yp = np.sin(thetaR)
            self.__shape[i * 2] = QPointF(xp, yp)

            xc = np.cos(thetar) * self.__r
            yc = np.sin(thetar) * self.__r
            self.__shape[i * 2 + 1] = QPointF(xc, yc)
