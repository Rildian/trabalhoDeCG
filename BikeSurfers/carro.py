import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Carro:
    def __init__(self, initial_position = glm.vec3(0.0, 0.0, 0.0), comeco = glm .vec3(0,0,0), fim =glm .vec3(-1,0,0)):
        self.position = initial_position
        self.valor = glm.vec3(0, 0, 0)
        self.angulo_roda = 0.0
        self.inicio = comeco  + self.position 
        self.fim = fim  + self.position 
        self.vertices = [
            [-1, -1, -1], 
            [1, -1, -1], 
            [1, 1, -1],   
            [-1, 1, -1],  
            [-1, -1, 1],  
            [1, -1, 1],  
            [1, 1, 1],     
            [-1, 1, 1],    
        ]
        self.faces = [
            [0, 1, 2, 3], 
            [4, 5, 6, 7], 
            [0, 1, 5, 4], 
            [2, 3, 7, 6],  
            [0, 3, 7, 4],  
            [1, 2, 6, 5], 
        ]
        
        self.lados_roda = 8
        self.vertices_roda = self.calcular_vertices_roda()

    def get_trajeto(self):
        return self.inicio, self.fim

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
        return self.position 

    def update(self, p):
        self.position = glm.mix(self.inicio ,self.fim, p)
        self.angulo_roda = (self.angulo_roda + 2) % 360

    def desenhar_roda(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo_roda, 0, 0, 1)
        glRotatef(90, 1, 0, 0)
        
        glColor3f(0.3, 0.3, 0.3)
        faces = self.calcular_faces_roda()

        glBegin(GL_POLYGON)
        for vertex in faces[0]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()

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
        glBegin(GL_POLYGON)
        for vertex in faces[1]:
            glVertex3fv(self.vertices_roda[vertex])
        glEnd()
        
        glBegin(GL_QUADS)
        for face in faces[2:]:
            for vertex in face:
                glVertex3fv(self.vertices_roda[vertex])
        glEnd()

    def draw_chassi(self,x, y, z, tam):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(12 * tam, 3 * tam, 5 * tam)

        glColor3f(0.3, 1, 0.3)
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glVertex3fv(self.vertices[vertex]) 
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(x+2, y+4, z)
        glScale(10 * tam, 3 * tam, 5 * tam)

        glColor3f(0.3, 1, 0.3)
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glVertex3fv(self.vertices[vertex]) 
        glEnd()
        glPopMatrix()

    def draw(self):
        pos = self.position 

        self.draw_chassi(pos[0], pos[1] + 5, pos[2], 1)
        self.desenhar_roda(pos[0] - 6, pos[1] + 3 , pos[2] - 6, 8)  
        self.desenhar_roda(pos[0] - 6, pos[1 ]+ 3 , pos[2] + 6, 8)  

        self.desenhar_roda(pos[0] + 6, pos[1] + 3, pos[2] - 6, 8) 
        self.desenhar_roda(pos[0] + 6, pos[1] + 3, pos[2] + 6, 8) 