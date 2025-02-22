import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from caminhao import Caminhao
from moto_obs import Moto
from chao import Chao
from carro import Carro

class Obstaculos:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position
        self.valor = initial_position
        self.p = 0.0
        self.comeco = glm.vec3(800, 0, 0)
        self.fim = glm.vec3(-800, 0, 0)
        self.chao = Chao()
        self.veloc = 0.001
        self.matriz = []
        
        self.caminhoes = [ 
        ]

        self.motos = [
        ]

        self.carros = [
            
        ]

    def mover(self, x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x
        elif self.p <= 1:
            self.p = 0
            self.veloc += 0.0001

    def set_obstaculos(self):
        print(self.matriz)
        for z in range (len(self.matriz)):
            for x in range(len(self.matriz[z])):
                if self.matriz[z][x] == 1:
                    moto = Moto((self.position[0] + (x*50 - 400), self.position[1] , self.position[2] + ((z*18 - 18)*(-1))), self.comeco, self.fim)
                    self.motos.append(moto)
                if self.matriz[z][x] == 2:
                    carro = Carro((self.position[0] + (x*50 - 400), self.position[1] , self.position[2] + ((z*18 - 18)*(-1))), self.comeco, self.fim)
                    self.carros.append(carro)
                if self.matriz[z][x] == 3:
                    caminhao = Caminhao((self.position[0] + (x*50 - 400), self.position[1]+ 3.5 , self.position[2] + ((z*18 - 18)*(-1))), self.comeco, self.fim)
                    self.caminhoes.append(caminhao)

    def set_matriz(self, x):
        self.matriz = x

    def reiniciar(self):
        self.caminhoes = []
        self.carros = []
        self.motos = []
        self.valor = [0,0,0]
        self.p = 0

    def get_posicao(self):
        return self.position + self.valor
    
    def get_p(self):
        return self.p

    def update(self):
        self.valor = glm.mix(self.comeco, self.fim, self.p)
        if len(self.caminhoes) > 0:
            for caminhao in self.caminhoes:
                caminhao.update(self.p)  # Atualiza cada caminhão
        if len(self.motos) > 0:
            for moto in self.motos:
                moto.update(self.p)
        if len(self.carros) > 0:
            for carro in self.carros:
                carro.update(self.p)
        self.mover(self.veloc)

    def draw(self):
        if len(self.caminhoes) > 0:
            for caminhao in self.caminhoes:
                caminhao.draw()  # Renderiza cada caminhão
        if len(self.motos) > 0:
            for moto in self.motos:
                moto.draw()
        if len(self.carros) > 0:
            for carro in self.carros:
                carro.draw()