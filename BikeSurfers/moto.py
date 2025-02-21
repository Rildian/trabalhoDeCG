import glm
from OpenGL.GL import *
import math
import numpy as np

class Moto:
    def __init__(self, initial_position=(0.0, 0.0, 0.0)):
        self.position = glm.vec3(*initial_position)
        self.p = 0.5  # Valor de mixagem para movimento lateral
        self.angulo_roda = 0.0
        self.valor = glm.vec3(0.0, 0.0, 0.0)
        
        # Parâmetros geométricos
        self.raio_roda = 0.5
        self.largura_roda = 0.2
        self.altura_assento = 4.7
        self.comprimento_guidon = 3.0
        self.angulo_chassi = 0.0

    def mover(self, x):
        """Controla o movimento lateral da moto"""
        self.p = max(0.0, min(1.0, self.p + x))

    def get_posicao(self):
        """Retorna a posição global da moto para detecção de colisões"""
        return tuple(self.position + self.valor)

    def update(self):
        """Atualiza a posição e animações da moto"""
        self.valor = glm.mix(
            glm.vec3(-360, 0, -23), 
            glm.vec3(-360, 0, 23), 
            self.p
        )
        self.angulo_roda = (self.angulo_roda - 2) % 360

    def desenhar_roda(self, offset):
        """Desenha uma roda na posição especificada"""
        glPushMatrix()
        glTranslatef(*offset)
        glScalef(5, 5, 5)
        glRotatef(self.angulo_roda, 0, 0, 1)
        glRotatef(90, 1, 0, 0)
        
        lados = 8
        vertices = []
        for i in range(lados):
            angulo = math.radians(i * (360 / lados))
            x = self.raio_roda * math.cos(angulo)
            z = self.raio_roda * math.sin(angulo)
            vertices.append((x, -self.largura_roda/2, z))
            vertices.append((x, self.largura_roda/2, z))
        
        glColor3f(0.3, 0.3, 0.3)
        # Bases
        glBegin(GL_POLYGON)
        for i in range(lados):
            glVertex3fv(vertices[i*2])
        glEnd()
        
        glBegin(GL_POLYGON)
        for i in range(lados):
            glVertex3fv(vertices[i*2+1])
        glEnd()
        
        # Lateral
        glBegin(GL_QUAD_STRIP)
        for i in range(lados+1):
            idx = i % lados
            glVertex3fv(vertices[idx*2])
            glVertex3fv(vertices[idx*2+1])
        glEnd()
        glPopMatrix()

    def desenhar_chassi(self):
        glPushMatrix()
        glTranslatef(3, 1.5, 0)
        glScalef(5, 5, 5)
        glColor3f(0.7, 0.0, 0.0)  # Vermelho

        # Ordem de rotações conforme o código original:
        glRotatef(self.angulo_chassi, 0, 1, 0)  # Rotação animada do chassi
        glRotatef(90, 1, 0, 0)                  # Rotação inicial no eixo X
        glRotatef(146.6, 0, 1, 0)               # Ajuste angular específico

        vertices = [
            (0, -0.15, -0.5),
            (1.5, -0.15, -0.5),
            (0, -0.15, 0.5),
            (0, 0.15, -0.5),
            (1.5, 0.15, -0.5),
            (0, 0.15, 0.5)
        ]

        # Bases
        glBegin(GL_TRIANGLES)
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[2])
        glEnd()

        glBegin(GL_TRIANGLES)
        glVertex3fv(vertices[3])
        glVertex3fv(vertices[4])
        glVertex3fv(vertices[5])
        glEnd()

        # Laterais
        glBegin(GL_QUADS)
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[4])
        glVertex3fv(vertices[3])
        
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[5])
        glVertex3fv(vertices[4])
        
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[3])
        glVertex3fv(vertices[5])
        glEnd()
        
        glPopMatrix()


    def desenhar_guidon(self):
        """Desenha o guidão da moto"""
        glPushMatrix()
        glTranslatef(3, 3, 0)
        glRotatef(20, 0, 0, 1)
        glColor3f(0.3, 0.3, 0.3)
        
        # Parte central
        self._desenhar_cubo((0, 0, 0), (4, 0.5, 0.5))
        
        # Parte horizontal
        glPushMatrix()
        glTranslatef(1.4, 1.5, 0)
        glRotatef(90, 0, 1, 0)
        self._desenhar_cubo((0, 0, 0), (3, 0.5, 0.5))
        glPopMatrix()
        
        # Alças
        for offset in [2, -2]:
            glPushMatrix()
            glTranslatef(1.4, 1.7, offset)
            glRotatef(90, 0, 1, 0)
            self._desenhar_cubo((0, 0, 0), (2, 0.5, 0.5))
            glPopMatrix()
        glPopMatrix()

    def _desenhar_cubo(self, pos, escala):
        """Método auxiliar para desenhar cubos"""
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(*escala)
        
        vertices = [
            (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
            (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)
        ]
        
        faces = [
            [0,1,2,3], [4,5,6,7],
            [0,1,5,4], [2,3,7,6],
            [0,3,7,4], [1,2,6,5]
        ]
        
        glBegin(GL_QUADS)
        for face in faces:
            for vert in face:
                glVertex3fv(vertices[vert])
        glEnd()
        glPopMatrix()

    def _desenhar_farol(self):
        """Desenha o farol dianteiro"""
        glPushMatrix()
        glTranslatef(4.2, 4.7, 0)
        glRotatef(90, 0, 1, 0)
        glColor3f(1, 1, 0)
        
        slices = stacks = 32
        radius = 0.8
        
        for i in range(stacks//2, stacks):
            lat0 = np.pi * (-0.5 + (i-1)/stacks)
            z0 = radius * np.sin(lat0)
            zr0 = radius * np.cos(lat0)
            
            lat1 = np.pi * (-0.5 + i/stacks)
            z1 = radius * np.sin(lat1)
            zr1 = radius * np.cos(lat1)
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices+1):
                lng = 2 * np.pi * j / slices
                x = np.cos(lng)
                y = np.sin(lng)
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()
        glPopMatrix()

    def _desenhar_escapamento(self):
        """Desenha o sistema de escapamento"""
        glPushMatrix()
        glTranslatef(-2, 1.5, 1)
        glColor3f(0.3, 0.3, 0.3)
        self._desenhar_cubo((0, 0, 0), (5, 1.5, 1))
        glPopMatrix()

    def draw(self):
        """Renderiza toda a moto"""
        pos = self.position + self.valor
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        
        # Rodas
        self.desenhar_roda((6, 1, 0))
        self.desenhar_roda((-3, 1, 0))
        
        # Chassi
        self.desenhar_chassi()
        
        # Peças laterais
        self._desenhar_cubo((4, 2, 0.4), (4, 0.5, 0.25))
        self._desenhar_cubo((4, 2, -0.4), (4, 0.5, 0.25))
        
        # Guidon
        self.desenhar_guidon()
        
        # Farol
        self._desenhar_farol()
        
        # Escapamento
        self._desenhar_escapamento()
        
        glPopMatrix()