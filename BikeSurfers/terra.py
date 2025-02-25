from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  


class Terra:
    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.angulo = 0.0
        self.texture = Texture(texture_path)
        self.movimento = 0
        self.contador= 0

    vertices = [
        [1, -1, -1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, -1, -1]
    ]


    tex_coords = [
        [(0.25, 0.0), (0.5, 0.0), (0.5, 0.33), (0.25, 0.33)]  
    ]

    def mover(self, x: float, y: float, z: float):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def update(self, velocidade):
        self.valor[0] -=velocidade

    def set_posicao(self, x, y, z):
        self.valor[0] = x
        self.valor[1] = y
        self.valor[2] = z


    def draw(self, x, y, z):
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        glScale(400, 400, 400)

        self.texture.bind()  
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_QUADS)
        for i, vertice in enumerate(self.vertices):
            glTexCoord2f(*self.tex_coords[0][i]) 
            glVertex3f(vertice[0], vertice[1], vertice[2])  
        glEnd()

        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()  

        glPopMatrix()
