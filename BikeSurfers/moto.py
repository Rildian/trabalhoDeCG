import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math
from roda import Roda
from corpo import Corpo

class Moto:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.roda = Roda()
        self.corpo = Corpo()

        self.angulo = 0.0
        self.valor = initial_position

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self):
        self.angulo = (self.angulo - 0.05) % 360

    def draw_roda(self, x, y, z, tamanho):
        self.roda.draw(x, y, z, tamanho)

    def draw_corpo(self, x, y, z, tamanho):
        self.corpo.draw(x, y, z, tamanho)

    def draw(self):
        # Desenha as rodas com o ajuste da posição
        self.draw_roda(self.valor[0] + 6, self.valor[1] + 1, self.valor[2] + 0.5, 5)
        self.draw_roda(self.valor[0] - 3, self.valor[1] + 1, self.valor[2] + 0.5, 5)
        # Desenha o corpo da moto
        self.draw_corpo(self.valor[0] + 3, self.valor[1] + 1.5, self.valor[2] + 0.5, 5)

    def mostrar(self):
        print(self.valor)
