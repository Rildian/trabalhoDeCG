from OpenGL.GL import *
import glm
from texture import Texture

class Menu:
    vertices = [
        [-1, 1, 0],
        [1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0] 
    ]

    tex_coords = [
        (0, 1), (1, 1), (1, 0), (0, 0) 
    ]

    def __init__(self, texture_path="menu.png", initial_position=glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.texture = Texture(texture_path)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
      
        glEnable(GL_TEXTURE_2D)
        self.texture.bind()  

        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord2f(*self.tex_coords[i])  
            glVertex3f(*self.vertices[i])  
        glEnd()

        self.texture.unbind()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
