from OpenGL.GL import *
from OpenGL.GLU import *
import glm
from texture import Texture  # Certifique-se de importar a classe Texture
import os

class Ceu:
    vertices = [
        [-0.5, -0.5, -0.5],  # Frente inferior esquerda
        [0.5, -0.5, -0.5],   # Frente inferior direita
        [0.5, 0.5, -0.5],    # Frente superior direita
        [-0.5, 0.5, -0.5],   # Frente superior esquerda
        [-0.5, -0.5, 0.5],   # Trás inferior esquerda
        [0.5, -0.5, 0.5],    # Trás inferior direita
        [0.5, 0.5, 0.5],     # Trás superior direita
        [-0.5, 0.5, 0.5],    # Trás superior esquerda
    ]

    faces = [
        [0, 1, 2, 3],  # Face frontal
        [5, 4, 7, 6],  # Face traseira
        [4, 5, 1, 0],  # Face inferior
        [3, 2, 6, 7],  # Face superior
        [4, 0, 3, 7],  # Face esquerda (ajustada)
        [1, 5, 6, 2],  # Face direita (ajustada)
    ]

    tex_coords = [
    [(0.25, 0.33), (0.5, 0.33), (0.5, 0.66), (0.25, 0.66)],  # Frente
    [(0.75, 0.33), (1.0, 0.33), (1.0, 0.66), (0.75, 0.66)],  # Trás
    [(0.25, 0.0), (0.5, 0.0), (0.5, 0.33), (0.25, 0.33)],  # Inferior
    [(0.255, 0.66), (0.495, 0.66), (0.495, 1.0), (0.255, 1.0)],  # Superior
    [(0.0, 0.33), (0.25, 0.33), (0.25, 0.66), (0.0, 0.66)],  # Esquerda (Ajustado)
    [(0.5, 0.33), (0.75, 0.33), (0.75, 0.66), (0.5, 0.66)],  # Direita (Ajustado)
    ]


    def __init__(self, texture_path="textura.png", initial_position= glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.valor = glm.vec3(0.0, 0.0, 0.0)
        self.angulo = 0.0
        self.texture = Texture(texture_path)

    def set_posicao(self, z):
        self.valor[2] += z

    def update(self):
        self.angulo = (self.angulo + 0.03) % 360

    def draw(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo, 0, 1, 0)  # Rotação 3D ao redor do eixo Y

        self.texture.bind()  # Ativa a textura
        glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coords[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.vertices[vertex])  # Define a posição do vértice
        glEnd()

        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()  # Desativa a textura

        glPopMatrix()
