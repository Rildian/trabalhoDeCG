from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  # Certifique-se de importar a classe Texture
import math

class Chao:
    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.texture = Texture(texture_path)
        self.movimento = 0
        self.contador= 0

    # Definição dos vértices do chão
    vertices = [
        [400, -1, -25],
        [400, -1, 25],
        [-400, -1, 25],
        [-400, -1, -25]
    ]

    # Coordenadas de textura (UV) para o chão
    tex_coords = [
        [(1, 0), (1, 1), (0, 1), (0, 0)]  # Apenas uma face, com 4 vértices
    ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self, velocidade):
        self.valor[0] -= velocidade

    def set_posicao(self, x, y, z):
        self.valor[0] = x
        self.valor[1] = y
        self.valor[2] = z

    def draw(self, x, y, z):
        glPushMatrix()
        # Movimentação do objeto
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)

        self.texture.bind()  # Ativa a textura
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_QUADS)
        for i, vertice in enumerate(self.vertices):
            # Aplica a coordenada de textura para cada vértice
            glTexCoord2f(*self.tex_coords[0][i])  # Mapeia a coordenada UV
            glVertex3f(vertice[0], vertice[1], vertice[2])  # Define a posição do vértice
        glEnd()

        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()  # Desativa a textura

        glPopMatrix()
