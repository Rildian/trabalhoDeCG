from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  # Certifique-se de importar a classe Texture
import os

class Peca:
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
        [4, 5, 6, 7],  # Face traseira
        [0, 1, 5, 4],  # Face inferior
        [2, 3, 7, 6],  # Face superior
        [0, 3, 7, 4],  # Face esquerda
        [1, 2, 6, 5],  # Face direita
    ]

    tex_coords = [
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Frente
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Trás
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Inferior
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Superior
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Esquerda
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # Direita
    ]

    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.eixo = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.texture = Texture(texture_path)

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    

    def draw(self, x, y, z, tamanho_x, tamanho_y, tamanho_z):
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        glRotatef(-25, 0, 0, 1)  # Rotação 3D ao redor do eixo Y
        glScale(1 * tamanho_x, 1 * tamanho_y, 1 * tamanho_z)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coords[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.vertices[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()
