import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from caminhao import Caminhao
from chao import Chao

class Obstaculos:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position
        self.valor = initial_position
        self.p = 0.0
        self.comeco = glm.vec3(800, 0, 0)
        self.fim = glm.vec3(-800, 0, 0)
        self.chao = Chao()
        self.veloc = 0.001
        
        self.caminhoes = [
            Caminhao([
                self.position[0] + self.valor[0] + 50,
                self.position[1] + self.valor[1] + 3.5,
                self.position[2] + self.valor[2] - 16
            ], self.comeco, self.fim),

            Caminhao([
                self.position[0] + self.valor[0] + 200 ,
                self.position[1] + self.valor[1] + 3.5,
                self.position[2] + self.valor[2] + 0
            ], self.comeco, self.fim)
        ]

    def mover(self, x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x
        elif self.p <= 1:
            self.p = 0
            self.veloc += 0.0001

    def get_posicao(self):
        return self.position + self.valor
    
    def get_p(self):
        return self.p

    def update(self):
        self.valor = glm.mix(self.comeco, self.fim, self.p)
        for caminhao in self.caminhoes:
            caminhao.update(self.p)  # Atualiza cada caminhão
        self.mover(self.veloc)

    def draw(self):
        for caminhao in self.caminhoes:
            caminhao.draw()  # Renderiza cada caminhão
