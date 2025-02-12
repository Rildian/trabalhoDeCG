import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math

class Moto:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.vertices_roda = self.calcular_vertices_roda()
        self.vertices_corpo = self.calcular_vertices_corpo()
        self.angulo = 0.0
        self.valor = initial_position
    

    faces_roda= [
        [0, 1, 2, 3, 4, 5],  # Base inferior
        [6, 7, 8, 9, 10, 11],  # Base superior
        [0, 1, 7, 6], [1, 2, 8, 7], [2, 3, 9, 8], 
        [3, 4, 10, 9], [4, 5, 11, 10], [5, 0, 6, 11]  # Laterais
    ]
    
    vertices_cubo= [
        [-0.5, -0.5, -0.5],  # Frente inferior esquerda
        [0.5, -0.5, -0.5],   # Frente inferior direita
        [0.5, 0.5, -0.5],    # Frente superior direita
        [-0.5, 0.5, -0.5],   # Frente superior esquerda
        [-0.5, -0.5, 0.5],   # Trás inferior esquerda
        [0.5, -0.5, 0.5],    # Trás inferior direita
        [0.5, 0.5, 0.5],     # Trás superior direita
        [-0.5, 0.5, 0.5],    # Trás superior esquerda
    ]

    faces_cupo = [
        [0, 1, 2, 3],  # Face frontal
        [4, 5, 6, 7],  # Face traseira
        [0, 1, 5, 4],  # Face inferior
        [2, 3, 7, 6],  # Face superior
        [0, 3, 7, 4],  # Face esquerda
        [1, 2, 6, 5],  # Face direita
    ]

    faces_corpo = [
        [0, 1, 2],  # Base inferior
        [3, 4, 5],  # Base superior
        [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]  # Laterais
    ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def calcular_vertices_roda(self):
        """Calcula os vértices do prisma hexagonal."""
        altura = 0.1
        raio = 0.5
        vertices = []
        
        # Base inferior
        for i in range(6):
            angulo = math.radians(i * 60)
            vertices.append([raio * math.cos(angulo), -altura / 2, raio * math.sin(angulo)])
        
        # Base superior
        for i in range(6):
            angulo = math.radians(i * 60)
            vertices.append([raio * math.cos(angulo), altura / 2, raio * math.sin(angulo)])
        
        return vertices
    

    def calcular_vertices_corpo(self):
        """Calcula os vértices do prisma triangular retângulo."""
        altura = 0.5
        base = 1.5
        profundidade = 1.0  # Comprimento do prisma
        
        vertices = [
            [0, -altura / 2, -profundidade / 2],  # Base inferior esquerda
            [base, -altura / 2, -profundidade / 2],  # Base inferior direita
            [0, -altura / 2, profundidade / 2],  # Base inferior frente
            [0, altura / 2, -profundidade / 2],  # Topo esquerda
            [base, altura / 2, -profundidade / 2],  # Topo direita
            [0, altura / 2, profundidade / 2]  # Topo frente
        ]
        return vertices


    def draw_roda(self, x, y, z, tamanho):
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotate(self.angulo, 0, 0, 1)  # Rotação 3D ao redor do eixo Y
        glRotate(90, 1, 0, 0)

        glBegin(GL_POLYGON)
        for vertex in self.faces_roda[0]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()

        glBegin(GL_POLYGON)
        for vertex in self.faces_roda[1]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.faces_roda[2:]:
            for vertex in face:
                glVertex3fv(self.vertices_roda[vertex])
        glEnd()


        glPopMatrix()


    def draw_corpo(self, x, y, z, tamanho):
        glColor3f(0,0.5,0.5)
        glPushMatrix()
        glTranslatef(self.position[0] +  x, self.position[1] + y, self.position[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotate(90, 1, 0, 0)  # Rotação 3D ao redor do eixo Y
        glRotate(155, 0, 1, 0)  # Rotação 3D ao redor do eixo Y

        glBegin(GL_TRIANGLES)
        for vertex in self.faces_corpo[0]:
            glVertex3fv(self.vertices_corpo[vertex])
        glEnd()

        glBegin(GL_TRIANGLES)
        for vertex in self.faces_corpo[1]:
            glVertex3fv(self.vertices_corpo[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.faces_corpo[2:]:
            for vertex in face:
                glVertex3fv(self.vertices_corpo[vertex])
        glEnd()

        glPopMatrix()

    def update(self):
        self.angulo = (self.angulo - 0.05) % 360

    def draw(self):
        self.draw_roda(self.valor[0] + 2.5,self.valor[1] + -1, self.valor[2] + 0,5)
        self.draw_roda(self.valor[0] + -6, self.valor[1] + -1, self.valor[2] + 0,5)
        self.draw_corpo(self.valor[0] + 0, self.valor[1] + 0.5, self.valor[2] + 0,5)
    

    def mostrar(self):
        print(self.vertices)
