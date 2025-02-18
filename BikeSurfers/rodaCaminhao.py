from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Roda:
    def __init__(self, initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.lados = 8
        self.vertices = self.calcular_vertices()

    def calcular_vertices(self):
        """Calcula os vértices do prisma com base no número de lados."""
        altura = 0.2
        raio = 0.5
        vertices = []

        # Base inferior
        for i in range(self.lados):
            angulo = math.radians(i * (360 / self.lados))
            vertices.append([raio * math.cos(angulo), -altura / 2, raio * math.sin(angulo)])

        # Base superior
        for i in range(self.lados):
            angulo = math.radians(i * (360 / self.lados))
            vertices.append([raio * math.cos(angulo), altura / 2, raio * math.sin(angulo)])

        return vertices

    def calcular_faces(self):
        """Define as faces corretamente com base na quantidade de lados."""
        faces = []

        # Base inferior
        faces.append(list(range(self.lados)))

        # Base superior
        faces.append(list(range(self.lados, 2 * self.lados)))

        # Laterais
        for i in range(self.lados):
            proximo = (i + 1) % self.lados
            faces.append([i, proximo, proximo + self.lados, i + self.lados])

        return faces

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self):
        self.angulo = (self.angulo + 2) % 360

    def draw(self, x, y, z, tamanho):
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, self.position[1] + self.valor[1] + y, self.position[2] + self.valor[2] + z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo, 0, 0, 1)  # Rotação 3D ao redor do eixo Z
        glRotatef(90, 1, 0, 0)  # Alinha a roda corretamente

        faces = self.calcular_faces()

        # Desenha a base inferior
        glBegin(GL_POLYGON)
        for vertex in faces[0]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        # Desenha a base superior
        glBegin(GL_POLYGON)
        for vertex in faces[1]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        # Desenha as faces laterais
        glBegin(GL_QUADS)
        for face in faces[2:]:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glPopMatrix()
