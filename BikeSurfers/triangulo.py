from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  # Certifique-se de importar a classe Texture
import math

class PrismaTriangular:
    def __init__(self,  initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.vertices = self.calcular_vertices()

    def calcular_vertices(self):
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

    faces = [
        [0, 1, 2],  # Base inferior
        [3, 4, 5],  # Base superior
        [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]  # Laterais
    ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self):
        self.angulo = (self.angulo + 0.03) % 360

    def draw(self, x, y, z, tamanho):
        glColor3f(0,0.5,0.5)
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, self.position[1] + self.valor[1] + y, self.position[2] + self.valor[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotate(self.angulo, 0, 1, 0)  # Rotação 3D ao redor do eixo Y
        glRotate(90, 1, 0, 0)  # Rotação 3D ao redor do eixo Y
        glRotate(146.6, 0, 1, 0)  # Rotação 3D ao redor do eixo Y

        glBegin(GL_TRIANGLES)
        for vertex in self.faces[0]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_TRIANGLES)
        for vertex in self.faces[1]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.faces[2:]:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glPopMatrix()
