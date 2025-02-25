from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture 

class Cacto:
    def __init__(self, texture_path="textura.png", initial_position=[0.0, 0.0, 0.0]):
        self.position = initial_position.copy()
        self.valor = [0.0, 0.0, 0.0]
        self.texture = Texture(texture_path)

    vertices = [
        [0, 0, -2],
        [0, 5, -2],
        [0, 5, 2],
        [0, 0, 2]
    ]

    tex_coords = [
        [(1, 0), (1, 1), (0, 1), (0, 0)]  
    ]


    def update(self, velocidade):
        self.valor[0] -= velocidade

    def set_posicao(self, x, y, z):
        self.valor[0] = x
        self.valor[1] = y
        self.valor[2] = z

    def draw(self, x, y, z, tam):
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        
        glScale(tam, tam, tam)

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
 