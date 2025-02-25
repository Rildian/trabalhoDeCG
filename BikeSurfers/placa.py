from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture
import math

class Placa:
    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.texture = Texture(texture_path)
        
        self.vertices_placa = self.calcular_vertices()
        self.tex_coords_placa = self.calcular_tex_coords()
        
        self.vertices_poste = [
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
        ]
        self.faces_poste = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]

    def calcular_vertices(self, raio=0.5):
        vertices = []
        for i in range(8):
            angulo = math.radians(i * 45)
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            vertices.append([x, y, 0.0])
        return vertices

    def calcular_tex_coords(self):
        return [
            (0.1,0.66), (0.33,0.9), (0.66,0.9), (0.9, 0.66),
            (0.9, 0.33), (0.66,0.1), (0.33, 0.1), (0.1, 0.33)
        ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self, velocidade):
        self.valor[0] -= velocidade

    def set_posicao(self, x, y, z):
        self.valor = [x, y, z]

    def draw(self, x, y, z, tamanho):
        self._draw_placa(x, y, z, tamanho)
        self._draw_poste(x, y, z, tamanho)

    def _draw_placa(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(
            self.position[0] + self.valor[0] + x,
            self.position[1] + self.valor[1] + y + 2,  
            self.position[2] + self.valor[2] + z
        )
        glRotate(90, 0, 1, 0)
        glScale(tamanho/1.5, tamanho/1.5, 1/1.5)
        glRotate(self.angulo, 0, 0, 1)
        glRotate(22.5, 0, 0, 1)

        self.texture.bind()
        glEnable(GL_TEXTURE_2D)
        
        glBegin(GL_POLYGON)
        for i, vertice in enumerate(self.vertices_placa):
            glTexCoord2f(*self.tex_coords_placa[i])
            glVertex3f(*vertice)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()
        glPopMatrix()

    def _draw_poste(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(
            self.position[0] + self.valor[0] + x + 0.6,
            self.position[1] + self.valor[1] + y - 3.2,
            self.position[2] + self.valor[2] + z
        )
        glScale(tamanho * 0.1, tamanho * 1.5, tamanho * 0.1)
        glColor3f(0.3, 0.3, 0.3)
        
        glBegin(GL_QUADS)
        for face in self.faces_poste:
            for vertex in face:
                glVertex3fv(self.vertices_poste[vertex])
        glEnd()
        glPopMatrix()