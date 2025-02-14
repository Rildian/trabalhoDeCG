import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math
from roda import Roda
from corpo import Corpo
from peca import Peca
from guidon import Guidon
from esfera import Esfera
from escapamento import Escapamento

class Moto:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.roda = Roda()
        self.corpo = Corpo()
        self.peca = Peca()
        self.guidon = Guidon()
        self.farol = Esfera()
        self.escapamento = Escapamento()

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

    def draw_peca(self, x, y, z, a, b, c):
        self.peca.draw(x, y, z, a, b, c)

    def draw_guidon(self, x, y, z):
        self.guidon.draw(x, y, z)

    def draw_farol(self,raio, lat, lon, x, y, z):
        self.farol.draw(raio, lat, lon, x, y, z)
    
    def draw_escapamento(self, x, y, z, a, b, c):
        self.escapamento.draw(x, y, z, a, b, c)

    def draw(self):
        self.draw_roda(self.valor[0] + 6, self.valor[1] + 1, self.valor[2] + 0, 5)
        self.draw_roda(self.valor[0] - 3, self.valor[1] + 1, self.valor[2] + 0, 5)
        self.draw_corpo(self.valor[0] + 3, self.valor[1] + 1.5, self.valor[2] + 0, 5)
        self.draw_peca(self.valor[0] + 4, self.valor[1] + 2, self.valor[2] + 0.4, 4, 0.5, 0.25)
        self.draw_peca(self.valor[0] + 4, self.valor[1] + 2, self.valor[2] + -0.4, 4, 0.5, 0.25)
        self.draw_guidon(self.valor[0] + 4, self.valor[1] + 4, self.valor[2] + 0)
        self.draw_farol(1, 10, 10, self.valor[0] + 6, self.valor[1] + 4.7, self.valor[2] + 0)
        self.draw_escapamento(self.valor[0] + -2, self.valor[1] + 3, self.valor[2] + 1, 5, 1.5, 1)


    def mostrar(self):
        print(self.valor)
