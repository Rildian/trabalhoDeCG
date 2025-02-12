from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  # Certifique-se de importar a classe Texture
import math

class PrismaHexagonal:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.vertices = self.calcular_vertices()

    def calcular_vertices(self):
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

    faces = [
        [0, 1, 2, 3, 4, 5],  # Base inferior
        [6, 7, 8, 9, 10, 11],  # Base superior
        [0, 1, 7, 6], [1, 2, 8, 7], [2, 3, 9, 8], 
        [3, 4, 10, 9], [4, 5, 11, 10], [5, 0, 6, 11]  # Laterais
    ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self):
        self.angulo = (self.angulo + 0.03) % 360

    def draw(self, x, y, z, tamanho):
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, self.position[1] + self.valor[1] + y, self.position[2] + self.valor[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotate(self.angulo, 0, 0, 1)  # Rotação 3D ao redor do eixo Y
        glRotate(90, 1, 0, 0)

        glBegin(GL_POLYGON)
        for vertex in self.faces[0]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_POLYGON)
        for vertex in self.faces[1]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.faces[2:]:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()


        glPopMatrix()
