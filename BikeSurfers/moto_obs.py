
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math

class Moto:
    def __init__(self, initial_position= glm.vec3(0.0, 0.0, 0.0),comeco = glm .vec3(0,0,0), fim = glm .vec3(-1,0,0)):
        self.position = initial_position
        self.angulo = 0.0
        self.comeco = comeco + self.position 
        self.fim = fim + self.position 
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
            [-0.5, -0.5, -0.5],  # Frente inferior esquerda
            [0.25, -0.25, -0.25],   # Frente inferior direita
            [0.25, 0.25, -0.25],    # Frente superior direita
            [-0.5, 0.5, -0.5],   # Frente superior esquerda
            [-0.5, -0.5, 0.5],   # Trás inferior esquerda
            [0.25, -0.25, 0.25],    # Trás inferior direita
            [0.25, 0.25, 0.25],     # Trás superior direita
            [-0.5, 0.5, 0.5],    # Trás superior esquerda
        ]

        self.verticesPeca = [
            [-0.5, -0.5, -0.5],  # Frente inferior esquerda
            [0.5, -0.5, -0.5],   # Frente inferior direita
            [0.5, 0.5, -0.5],    # Frente superior direita
            [-0.5, 0.5, -0.5],   # Frente superior esquerda
            [-0.5, -0.5, 0.5],   # Trás inferior esquerda
            [0.5, -0.5, 0.5],    # Trás inferior direita
            [0.5, 0.5, 0.5],     # Trás superior direita
            [-0.5, 0.5, 0.5],    # Trás superior esquerda
        ]

        self.facesPeca = [
            [0, 1, 2, 3],  # Face frontal
            [4, 5, 6, 7],  # Face traseira
            [0, 1, 5, 4],  # Face inferior
            [2, 3, 7, 6],  # Face superior
            [0, 3, 7, 4],  # Face esquerda
            [1, 2, 6, 5],  # Face direita
        ]

        self.tex_coordsPeca = [
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Frente
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Trás
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Inferior
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Superior
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Esquerda
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Direita
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

        # Base inferior
        for i in range(lados):
            angulo = math.radians(i * (360 / lados))
            vertices.append([raio * math.cos(angulo), -altura / 2, raio * math.sin(angulo)])

        # Base superior
        for i in range(lados):
            angulo = math.radians(i * (360 / lados))
            vertices.append([raio * math.cos(angulo), altura / 2, raio * math.sin(angulo)])

        return vertices

    def calcular_faces_roda(self, lados):
        faces = []

        # Base inferior
        faces.append(list(range(lados)))

        # Base superior
        faces.append(list(range(lados, 2 * lados)))

        # Laterais
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

    def get_posicao(self):
        return self.position + self.valor
    
    def get_trajeto(self):
        return self.comeco, self.fim

    def update(self, p):
        self.position = glm.mix(self.comeco ,self.fim, p)
        self.angulo = (self.angulo - 2) % 360

    def draw_roda(self, x, y, z, tamanho):
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        glTranslatef(x, y, z)
        glScale(tamanho, tamanho, tamanho)
        glRotatef(self.angulo, 0, 0, 1)  
        glRotatef(90, 1, 0, 0) 

        # Desenha a base inferior
        glBegin(GL_POLYGON)
        for vertex in self.facesRoda[0]:
            glVertex3fv(self.verticesRoda[vertex])
        glEnd()

        # Desenha a base superior
        glBegin(GL_POLYGON)
        for vertex in self.facesRoda[1]:
            glVertex3fv(self.verticesRoda[vertex])
        glEnd()

        # Desenha as faces laterais
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
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesEscapamento[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()

    def draw_peca(self, x, y, z, tamanho_x, tamanho_y, tamanho_z):
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glRotatef(-25, 0, 0, 1)  # Rotação 3D ao redor do eixo Y
        glScale(1 * tamanho_x, 1 * tamanho_y, 1 * tamanho_z)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesPeca[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()

    def draw_guidon(self,x, y, z):

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x,  y, z)
        glRotatef(50, 0, 0, 1)  # Rotação 3D ao redor do eixo Y
        glScale(4, 0.5, 0.5)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesPeca[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.5, 0)
        glRotatef(90, 0, 1, 0)  
        glScale(3, 0.5, 0.5)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesPeca[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.7, 2)
        glRotatef(90, 0, 1, 0)  
        glScale(2, 0.5, 0.5)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesPeca[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(x, y, z)
        glTranslatef(1.4, 1.7, -2)
        glRotatef(90, 0, 1, 0)  
        glScale(2, 0.5, 0.5)
       
        #self.texture.bind()  # Ativa a textura
        #glEnable(GL_TEXTURE_2D)

        # Coordenadas de textura (UV) para cada face
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesPeca):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coordsPeca[i][j])  # Aplica a coordenada de textura UV
                glVertex3fv(self.verticesPeca[vertex])  # Define a posição do vértice
        glEnd()

        #glDisable(GL_TEXTURE_2D)
        #self.texture.unbind()  # Desativa a textura

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
        glPushMatrix()  # Salva a matriz de transformação atual
        glTranslatef(self.position[0], self.position[1], self.position[2])  # Move a moto para a posição correta
        glRotatef(180, 0, 1, 0)  # Rotaciona 180 graus no eixo Y
        
        self.draw_roda(6, 1, 0, 5)
        self.draw_roda(-3, 1, 0, 5)
        self.draw_chassi(3, 1.5, 0, 5)
        self.draw_peca(4, 2, 0.4, 4, 0.5, 0.25)
        self.draw_peca(4, 2, -0.4, 4, 0.5, 0.25)
        self.draw_guidon(4, 4, 0)
        self.draw_farol(1, 10, 10, 6, 4.5, 0)
        self.draw_escapamento(-2, 3, 1, 5, 1.5, 1)

        glPopMatrix()  # Restaura a matriz original para evitar que outras partes da cena sejam afetadas
