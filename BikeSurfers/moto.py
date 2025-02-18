import glfw
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math
from roda import Roda
from corpo_moto import Corpo
from peca_moto import Peca
from guidon_moto import Guidon
from esfera import Esfera
from escapamento import Escapamento

class Moto:
    def __init__(self, initial_position= glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.roda = Roda()
        self.corpo = Corpo()
        self.peca = Peca()
        self.guidon = Guidon()
        self.farol = Esfera()
        self.escapamento = Escapamento()
        self.p = 0.5

        self.angulo = 0.0
        self.valor = glm.vec3(0,0,0)

    def mover(self,x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x

    def get_posicao(self):
        return self.position + self.valor

    def update(self):
        self.valor = glm.mix([-360,0,-23],[-360,0,23], self.p)
        print(f"Moto{self.valor}")
        self.roda.update()

    def draw(self):
        self.roda.draw(self.position[0] + self.valor[0] + 6, self.position[1] + self.valor[1] + 1,self.position[2] + self.valor[2] + 0, 5)
        self.roda.draw(self.position[0] + self.valor[0] - 3, self.position[1] +  self.valor[1] + 1,self.position[2] +  self.valor[2] + 0, 5)
        self.corpo.draw(self.position[0] + self.valor[0] + 3, self.position[1] + self.valor[1] + 1.5,self.position[2] +  self.valor[2] + 0, 5)
        self.peca.draw(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 2,self.position[2] + self.valor[2] + 0.4, 4, 0.5, 0.25)
        self.peca.draw(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 2,self.position[2] + self.valor[2] + -0.4, 4, 0.5, 0.25)
        self.guidon.draw(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 4,self.position[2] + self.valor[2] + 0)
        self.farol.draw(1, 10, 10, self.position[0] + self.valor[0] + 6, self.position[1] + self.valor[1] + 4.7, self.position[2] + self.valor[2] + 0)
        self.escapamento.draw(self.position[0] + self.valor[0] + -2, self.position[1] + self.valor[1] + 3, self.position[2] + self.valor[2] + 1, 5, 1.5, 1)


    def mostrar(self):
        print(self.valor)
