import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math
from placa import Placa
from chao import Chao
from ceu import Ceu
from terra import Terra
from cacto import Cacto
from outdoor import Outdoor
import random

class Cenario:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position
        self.valor = initial_position

        self.chao1 = Chao(texture_path = "asfalto.jpg")
        self.chao2 = Chao(texture_path = "asfalto.jpg")

        self.ceu = Ceu(texture_path = "skybox.png")
        self.pos = [-800,0,0]
        self.pos3 = [-1600, 0, 0]
        self.pos2 = [0,0,0]

        self.terra1 = Terra(texture_path = "skybox.png")
        self.terra2 = Terra(texture_path = "skybox.png")

        self.cacto = Cacto(texture_path = "cacto.png")
        self.cacto2 = Cacto(texture_path = "cacto.png")
        self.velocidade = 1

        self.cactos_posicoes = self.gerar_posicoes_cactos()
        self.outdoor = Outdoor(texture_path = "OUT door.png")
        self.placa = Placa(texture_path="Pare.jpg")

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def floor_loop(self):
        self.pos[0] -= self.velocidade
        self.pos2[0] -= self.velocidade
        self.pos3[0] -= self.velocidade
        if self.pos[0] == -1600:
            self.chao1.set_posicao(800, 0, 0)
            self.terra1.set_posicao(800,0,0)
            self.cacto.set_posicao(800, 0, 0)
            self.pos[0] = 0
        if self.pos2[0] == -1600:
            self.chao2.set_posicao(0, 0, 0)
            self.terra2.set_posicao(0, 0, 0)
            self.placa.set_posicao(0, 0, 0)
            self.cacto2.set_posicao(800, 0, 0)
            self.pos2[0] = 0 
        if self.pos3[0] == -10000:
            self.outdoor.set_posicao(0, 0, 0)
            self.pos3[0] = 0 

    def update(self):
        self.floor_loop()
        self.chao1.update(self.velocidade)
        self.chao2.update(self.velocidade)
        self.terra1.update(self.velocidade)
        self.terra2.update(self.velocidade)
        self.placa.update(self.velocidade)
        self.cacto.update(self.velocidade)
        self.cacto2.update(self.velocidade)
        self.outdoor.update(self.velocidade)

    def gerar_posicoes_cactos(self):
        posicoes = []
        for _ in range(20):
            x = random.uniform(-390, 390)
            
            while True:
                z = random.uniform(-390, 390)
                if z < -30 or z > 30:  
                    break

            posicoes.append((x, z))  
        return posicoes

    def draw(self):
        self.placa.draw(self.valor[0] + 800, self.valor[1] + 10, self.valor[2] + 25, 10)
        self.ceu.draw(self.valor[0] + 0, self.valor[1] + 0, self.valor[2] + 0 , 800)
        self.chao1.draw(0 ,0, 0)
        self.chao2.draw(800 ,0, 0)
        self.terra1.draw(0,398,0)
        self.terra2.draw(800,398,0)
        self.outdoor.draw(4000,40,-100,30)

        for x, z in self.cactos_posicoes:
            self.cacto.draw(self.valor[0] + x, self.valor[1] + 0, self.valor[2] + z, 5)
            self.cacto2.draw(self.valor[0] + x, self.valor[1] + 0, self.valor[2] + z, 5)
    def mostrar(self):
        print(self.valor)
