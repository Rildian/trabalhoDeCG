import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from container import Container
from rodaCaminhao import Roda
from corpoCaminhao import Corpo

class Caminhao:
    def __init__(self, initial_position= glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.roda = Roda()
        self.corpo = Corpo()
        self.conteiner = Container()
        self.valor = glm.vec3(0,0,0)

    def mover(self,x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x

    def get_posicao(self):
        return self.position + self.valor

    def update(self,c ,f, p):
        self.valor = glm.mix(c + self.position, f + self.position, p)
        print(f"Caminhao{self.valor + self.position}")
        self.roda.update()

    def draw(self):
        self.conteiner.draw(self.position[0] + self.valor[0], self.position[1] + self.valor[1] , self.position[2] + self.valor[2], 1, 1, 1)
        self.corpo.draw(self.position[0] + self.valor[0] - 25, self.position[1] + self.valor[1] - 2 , self.position[2] + self.valor[2], 1)
        self.roda.draw(self.position[0] + self.valor[0] - 25, self.position[1] + self.valor[1] - 5 , self.position[2] + self.valor[2] - 6, 10)
        self.roda.draw(self.position[0] + self.valor[0] + 10, self.position[1] + self.valor[1] - 5 , self.position[2] + self.valor[2] +  6, 10)
        self.roda.draw(self.position[0] + self.valor[0] + 10, self.position[1] + self.valor[1] - 5 , self.position[2] + self.valor[2] -  6, 10)
        self.roda.draw(self.position[0] + self.valor[0] - 25, self.position[1] + self.valor[1] - 5 , self.position[2] + self.valor[2] +  6, 10)
