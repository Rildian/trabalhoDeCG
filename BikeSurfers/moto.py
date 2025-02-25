import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math

class Moto:
    def __init__(self, initial_position= glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.p = 0.5
        self.angulo = 0.0
        self.valor = glm.vec3(0,0,0)
        self.verticesRoda = self.calcular_vertices_roda(8)
        self.facesRoda = self.calcular_faces_roda(8)
        self.verticesChassi = self.calcular_vertices_chassi()
        self.chassiFaces = [
            [0, 1, 2], 
            [3, 4, 5],  
            [0, 1, 4, 3], 
            [1, 2, 5, 4], 
            [2, 0, 3, 5]  
        ]

        self.verticesEscapamento = [
            [-0.5, -0.5, -0.5], 
            [0.25, -0.25, -0.25],  
            [0.25, 0.25, -0.25],   
            [-0.5, 0.5, -0.5],  
            [-0.5, -0.5, 0.5],  
            [0.25, -0.25, 0.25],   
            [0.25, 0.25, 0.25],    
            [-0.5, 0.5, 0.5],   
        ]

        self.verticesPeca = [
            [-0.5, -0.5, -0.5],  
            [0.5, -0.5, -0.5],   
            [0.5, 0.5, -0.5],    
            [-0.5, 0.5, -0.5],  
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],   
            [0.5, 0.5, 0.5],     
            [-0.5, 0.5, 0.5],    
        ]

        self.facesPeca = [
            [0, 1, 2, 3], 
            [4, 5, 6, 7],  
            [0, 1, 5, 4],  
            [2, 3, 7, 6],  
            [0, 3, 7, 4],  
            [1, 2, 6, 5],  
        ]

        self.tex_coordsPeca = [
            [(0, 0), (1, 0), (1, 1), (0, 1)],  
            [(0, 0), (1, 0), (1, 1), (0, 1)],  
            [(0, 0), (1, 0), (1, 1), (0, 1)], 
            [(0, 0), (1, 0), (1, 1), (0, 1)],  
            [(0, 0), (1, 0), (1, 1), (0, 1)],  
            [(0, 0), (1, 0), (1, 1), (0, 1)],  
        ]

    def calcular_vertices_chassi(self):
        altura = 0.3
        base = 1.5
        profundidade = 1.0  
        
        vertices = [
            [0, -altura / 2, -profundidade / 2], 
            [base, -altura / 2, -profundidade / 2],  
            [0, -altura / 2, profundidade / 2],  
            [0, altura / 2, -profundidade / 2], 
            [base, altura / 2, -profundidade / 2],  
            [0, altura / 2, profundidade / 2]  
        ]
        return vertices

    def calcular_vertices_roda(self,lados):
        altura = 0.2
        raio = 0.5
        vertices = []

        for i in range(lados):
            angulo = math.radians(i * (360 / lados))
            vertices.append([raio * math.cos(angulo), -altura / 2, raio * math.sin(angulo)])

        for i in range(lados):
            angulo = math.radians(i * (360 / lados))
            vertices.append([raio * math.cos(angulo), altura / 2, raio * math.sin(angulo)])

        return vertices

    def calcular_faces_roda(self, lados):
        faces = []

        faces.append(list(range(lados)))

        faces.append(list(range(lados, 2 * lados)))

        for i in range(lados):
            proximo = (i + 1) % lados
            faces.append([i, proximo, proximo + lados, i + lados])

        return faces

    def pedaco(self, raio, slices, stacks):
        for i in range(stacks // 2):
            lat0 = np.pi * (-0.5 + float(i)/ stacks)
            z0 = raio * np.sin(lat0)
            zr0 = raio * np.cos(lat0)

            lat1 = np.pi * (-0.5 + float(i + 1)/ stacks)
            z1 = raio * np.sin(lat1)
            zr1 = raio * np.cos(lat1)
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * np.pi* float(j) / slices
                x = np.cos(lng)
                y = np.sin(lng)
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()

    def esfera(self, raio, slices, stacks):
        for i in range(stacks):
            lat0 = np.pi * (-0.5 + float(i)/ stacks)
            z0 = raio * np.sin(lat0)
            zr0 = raio * np.cos(lat0)

            lat1 = np.pi * (-0.5 + float(i + 1)/ stacks)
            z1 = raio * np.sin(lat1)
            zr1 = raio * np.cos(lat1)
            glColor(1,1,0)
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * np.pi* float(j) / slices
                x = np.cos(lng)
                y = np.sin(lng)
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()

    def mover(self,x):
        if self.p + x >= 0 and self.p + x <= 1:
            self.p += x

    def get_posicao(self):
        return self.position + self.valor

    def update(self):
        self.valor = glm.mix([-360,0,-26],[-360,0,26], self.p)
        self.angulo = (self.angulo - 2) % 360

    def draw_roda(self, x, y, z, tamanho):
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo, 0, 0, 1)  
        glRotatef(90, 1, 0, 0) 

        glBegin(GL_POLYGON)
        for vertex in self.facesRoda[0]:
            glVertex3fv(self.verticesRoda[vertex])
        glEnd()

        glBegin(GL_POLYGON)
        for vertex in self.facesRoda[1]:
            glVertex3fv(self.verticesRoda[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.facesRoda[2:]:
            for vertex in face:
                glVertex3fv(self.verticesRoda[vertex])
        glEnd()

        glPopMatrix()

    def draw_chassi(self, x, y, z, tamanho):
        glColor3f(1, 0.3, 0.3)
        glPushMatrix()
        glTranslatef( x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotate(90, 1, 0, 0)  
        glRotate(146.6, 0, 1, 0)  

        glBegin(GL_TRIANGLES)
        for vertex in self.chassiFaces[0]:
            glVertex3fv(self.verticesChassi[vertex])
        glEnd()

        glBegin(GL_TRIANGLES)
        for vertex in self.chassiFaces[1]:
            glVertex3fv(self.verticesChassi[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in self.chassiFaces[2:]:
            for vertex in face:
                glVertex3fv(self.verticesChassi[vertex])
        glEnd()

        glPopMatrix()

    def draw_escapamento(self, x, y, z, tamanho_x, tamanho_y, tamanho_z):
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glScale(1 * tamanho_x, 1 * tamanho_y, 1 * tamanho_z)
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j]) 
                glVertex3fv(self.verticesEscapamento[vertex])  
        glEnd()

        glPopMatrix()

    def draw_peca(self, x, y, z, tamanho_x, tamanho_y, tamanho_z):
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glRotatef(-25, 0, 0, 1) 
        glScale(1 * tamanho_x, 1 * tamanho_y, 1 * tamanho_z)

        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j]) 
                glVertex3fv(self.verticesPeca[vertex]) 
        glEnd()


        glPopMatrix()

    def draw_guidon(self,x, y, z):

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x,  y, z)
        glRotatef(50, 0, 0, 1) 
        glScale(4, 0.5, 0.5)

        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j]) 
                glVertex3fv(self.verticesPeca[vertex])  
        glEnd()

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.5, 0)
        glRotatef(90, 0, 1, 0)  
        glScale(3, 0.5, 0.5)

        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  
                glVertex3fv(self.verticesPeca[vertex])  
        glEnd()

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.7, 2)
        glRotatef(90, 0, 1, 0)  
        glScale(2, 0.5, 0.5)

        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  
                glVertex3fv(self.verticesPeca[vertex])  
        glEnd()

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.7, -2)
        glRotatef(90, 0, 1, 0)  
        glScale(2, 0.5, 0.5)
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  
                glVertex3fv(self.verticesPeca[vertex]) 
        glEnd()
        
        glPopMatrix()

    def draw_farol(self, raio, slices, stacks, x, y, z):

        glPushMatrix()  
        glColor(0.3, 0.3, 0.3)
        glTranslatef(x -0.2, y, z)
        glRotate(90,0,1,0)
        glRotate(25,1,0,0)
        self.pedaco(raio, slices, stacks)
        glPopMatrix()
        
        glPushMatrix() 
        glColor(1,1,0) 
        glTranslatef(x, y, z)
        glScale(0.8,0.8,0.8)
        self.esfera(raio, slices, stacks)
        glPopMatrix()

    def draw(self):
        self.draw_roda(self.position[0] + self.valor[0] + 6, self.position[1] + self.valor[1] + 1,self.position[2] + self.valor[2] + 0, 5)
        self.draw_roda(self.position[0] + self.valor[0] - 3, self.position[1] +  self.valor[1] + 1,self.position[2] +  self.valor[2] + 0, 5)

        self.draw_chassi(self.position[0] + self.valor[0] + 3, self.position[1] + self.valor[1] + 1.5,self.position[2] +  self.valor[2] + 0, 5)

        self.draw_peca(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 2,self.position[2] + self.valor[2] + 0.4, 4, 0.5, 0.25)
        self.draw_peca(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 2,self.position[2] + self.valor[2] + -0.4, 4, 0.5, 0.25)

        self.draw_guidon(self.position[0] + self.valor[0] + 4,self.position[1] + self.valor[1] + 4,self.position[2] + self.valor[2] + 0)
        self.draw_farol(1, 10, 10, self.position[0] + self.valor[0] + 6, self.position[1] + self.valor[1] + 4.7, self.position[2] + self.valor[2] + 0)
        self.draw_escapamento(self.position[0] + self.valor[0] + -2, self.position[1] + self.valor[1] + 3, self.position[2] + self.valor[2] + 1, 5, 1.5, 1)


    def mostrar(self):
        print(self.valor)
