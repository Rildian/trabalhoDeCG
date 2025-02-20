import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Caminhao:
    def __init__(self, initial_position=glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.valor = glm.vec3(0, 0, 0)
        self.angulo_roda = 0.0
        self.angulo_corpo = 0.0
        
        # Rodas
        self.lados_roda = 8
        self.vertices_roda = self.calcular_vertices_roda()
        
        # Corpo (parte da frente)
        self.vertices_corpo = [
            [-6, -6, -8], [6, -6, -8], [6, 6, -8], [-6, 6, -8],
            [-6, -6, 8], [6, -6, 8], [6, 6, 8], [-6, 6, 8]
        ]
        self.faces_corpo = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 4, 7, 3], [5, 1, 2, 6]
        ]
        
        # Côntainer (parte de tras)
        self.vertices_container = [
            [-18, -8, -8], [18, -8, -8], [18, 8, -8], [-18, 8, -8],
            [-18, -8, 8], [18, -8, 8], [18, 8, 8], [-18, 8, 8]
        ]
        self.faces_container = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]

    def mover(self, x: float, y: float, z: float):
        self.valor += glm.vec3(x, y, z)

    def calcular_vertices_roda(self):
        altura = 0.2
        raio = 0.5
        vertices = []
        for i in range(self.lados_roda):
            angulo = math.radians(i * (360 / self.lados_roda))
            vertices.append([raio * math.cos(angulo), -altura/2, raio * math.sin(angulo)])
        for i in range(self.lados_roda):
            angulo = math.radians(i * (360 / self.lados_roda))
            vertices.append([raio * math.cos(angulo), altura/2, raio * math.sin(angulo)])
        return vertices

    def get_posicao(self):
        return self.position + self.valor

    def update(self, c=None, f=None, p=None):
        if c and f and p:
            self.valor = glm.mix(c + self.position, f + self.position, p)
        self.angulo_roda = (self.angulo_roda + 2) % 360
        self.angulo_corpo = (self.angulo_corpo + 0.03) % 360

    def desenhar_roda(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo_roda, 0, 0, 1)
        glRotatef(90, 1, 0, 0)
        
        # Desenho da roda
        glColor3f(0.3, 0.3, 0.3)
        faces = self.calcular_faces_roda()
        
        # Base inferior
        glBegin(GL_POLYGON)
        for vertex in faces[0]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()
        
        # Base superior e faces laterais
        self.desenhar_faces_roda(faces)
        glPopMatrix()

    def calcular_faces_roda(self):
        faces = [list(range(self.lados_roda))]
        faces.append(list(range(self.lados_roda, 2 * self.lados_roda)))
        for i in range(self.lados_roda):
            proximo = (i + 1) % self.lados_roda
            faces.append([i, proximo, proximo + self.lados_roda, i + self.lados_roda])
        return faces

    def desenhar_faces_roda(self, faces):
        # Base superior
        glBegin(GL_POLYGON)
        for vertex in faces[1]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()
        
        # Faces laterais
        glBegin(GL_QUADS)
        for face in faces[2:]:
            for vertex in face:
                glVertex3fv(self.vertices_roda[vertex])
        glEnd()

    def desenhar_corpo(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo_corpo, 0, 1, 0)
        glColor3f(0.5, 0.5, 0.5)
        
        glBegin(GL_QUADS)
        for face in self.faces_corpo:
            for vertex in face:
                glVertex3fv(self.vertices_corpo[vertex])
        glEnd()
        glPopMatrix()

    def desenhar_container(self, x, y, z, sx, sy, sz):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(sx * 0.5, sy * 0.5, sz * 0.5)
        glColor3f(0, 0.5, 0.5)
        
        glBegin(GL_QUADS)
        for face in self.faces_container:
            for vertex in face:
                glVertex3fv(self.vertices_container[vertex])
        glEnd()
        glPopMatrix()

    def draw(self):
        pos = self.position + self.valor
        # Container (parte de tras)
        self.desenhar_container(pos.x, pos.y, pos.z, 1, 1, 1)
        
        # Corpo (parte da frente)
        self.desenhar_corpo(pos.x - 15, pos.y +5.5, pos.z, 1)
        
        # Rodas
        self.desenhar_roda(pos.x - 15, pos.y - 5, pos.z - 8.5, 10)  # frente esquerda
        self.desenhar_roda(pos.x - 15, pos.y - 5, pos.z + 7.5, 10)  # frente direita

        self.desenhar_roda(pos.x + 10, pos.y-5, pos.z - 3.5, 10) #traseira esquerda
        self.desenhar_roda(pos.x + 10, pos.y-5, pos.z + 5.5, 10) # traseira direita