from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  # Certifique-se de importar a classe Texture
import math
from poste_placa import Poste_placa

class Placa:
    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.texture = Texture(texture_path)
        self.vertices = self.calcular_vertices()
        self.tex_coords = self.calcular_tex_coords()
        self.peca = Poste_placa()

    def calcular_vertices(self):
        """Calcula os vértices do octógono."""
        raio = 0.5
        vertices = []
        
        # Calcula os vértices do octógono
        for i in range(8):
            angulo = math.radians(i * (360/8))  # 360° / 8 lados = 45° por vértice
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            vertices.append([x, y, 0.0])  # Adiciona o vértice ao octógono
        
        return vertices

    def calcular_tex_coords(self):
        """Calcula as coordenadas de textura para o octógono."""
        # Coordenadas de textura para um octógono (mapeamento UV)
        return [
            (0.1,0.66), (0.33,0.9), (0.66,0.9), (0.9, 0.66), (0.9, 0.33), (0.66,0.1), (0.33, 0.1), (0.1, 0.33)
        ]



    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self, velocidade):
        self.valor[0] -= velocidade

    def draw_peca(self, x, y, z, a, b, c):
        self.peca.draw(x, y, z, a, b, c)

    def set_posicao(self, x, y, z):
        self.valor[0] = x
        self.valor[1] = y
        self.valor[2] = z

    def draw_placa(self, x,y,z,tamanho):
        glColor3f(1.0, 1.0, 1.0)  # Define a cor branca (a textura vai sobrescrever)
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, self.position[1] + self.valor[1] + y,self.position[2] + self.valor[2] + z)
        glRotate(90,0, 1, 0)
        glScale(tamanho/1.5, tamanho/1.5, 1/1.5)
        glRotate(self.angulo, 0, 0, 1) 
        glRotate(22.5, 0, 0, 1) 

        self.texture.bind()  # Ativa a textura
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_POLYGON)
        for i, vertice in enumerate(self.vertices):
            # Aplica a coordenada de textura para cada vértice
            glTexCoord2f(*self.tex_coords[i])  # Mapeia a coordenada UV
            glVertex3f(*vertice)  # Define a posição do vértice
        glEnd()
        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()  # Desativa a textura

        glPopMatrix()

    def draw(self, x, y, z, tamanho):
        self.draw_placa(x,y+2,z,tamanho)
        self.draw_peca(self.position[0] + self.valor[0] + x + 0.6, self.position[1] + self.valor[1] + y - 3.2, self.position[2] + self.valor[2] + z, tamanho * 0.1, tamanho * 1.5, tamanho * 0.1)
        

