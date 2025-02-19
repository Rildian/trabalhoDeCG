import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from caminhao import Caminhao
from chao import Chao

class Obstaculos:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position
        self.valor = initial_position
        self.caminhao = Caminhao([self.position[0] + self.valor[0] + 0, self.position[1] + self.valor[1] + 4.5, self.position[2] + self.valor[2] - 8])
        self.caminhao2 = Caminhao([self.position[0] + self.valor[0] + 100, self.position[1] + self.valor[1] + 4.5, self.position[2] + self.valor[2] + 8])
        self.p = 0
        self.comeco = glm.vec3(800, 0, 0)
        self.fim = glm.vec3(-800, 0, 0)
        self.chao = Chao()
        self.veloc = 0.001

    def mover(self,x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x
        elif self.p <= 1:
            self.p = 0

    def get_posicao(self):
        return self.position + self.valor

    def update(self):
        self.valor = glm.mix(self.comeco,self.fim, self.p)
        self.caminhao.update(self.comeco, self.fim, self.p)
        self.caminhao2.update(self.comeco, self.fim, self.p)
        self.mover(self.veloc)

    def draw(self):
        self.caminhao.draw()
        self.caminhao2.draw()

