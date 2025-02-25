from OpenGL.GL import *
from OpenGL.GLU import *
from texture import Texture  
import glm

class Outdoor:
    vertices = [
        [-1, -0.5, -0.01], 
        [1, -0.5, -0.01],   
        [1, 0.5, -0.01],    
        [-1, 0.5, -0.01],   
        [-1, -0.5, 0.01],  
        [1, -0.5, 0.01],   
        [1, 0.5, 0.01],     
        [-1, 0.5, 0.01],    
    ]

    faces = [
        [0, 1, 2, 3], 
        [4, 5, 6, 7], 
        [0, 1, 5, 4],
        [2, 3, 7, 6],  
        [0, 3, 7, 4], 
        [1, 2, 6, 5], 
    ]

    tex_coords = [
        [(0, 0), (1, 0), (1, 1), (0, 1)],  
        [(0, 0), (1, 0), (1, 1), (0, 1)],  
        [(0, 0), (1, 0), (1, 1), (0, 1)],  
        [(0, 0), (1, 0), (1, 1), (0, 1)],  
        [(0, 0), (1, 0), (1, 1), (0, 1)], 
        [(0, 0), (1, 0), (1, 1), (0, 1)],  
    ]

    verticesC = [
        [-0.5, -0.5, -0.5], 
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],    
        [-0.5, 0.5, -0.5],   
        [-0.5, -0.5, 0.5],   
        [0.5, -0.5, 0.5],    
        [0.5, 0.5, 0.5],   
        [-0.5, 0.5, 0.5],  
    ]

    facesC = [
        [0, 1, 2, 3],  
        [4, 5, 6, 7],  
        [0, 1, 5, 4],  
        [2, 3, 7, 6], 
        [0, 3, 7, 4],  
        [1, 2, 6, 5],  
    ]

    def __init__(self, texture_path="textura.png", initial_position=glm.vec3(0,0,0)):
        self.position = initial_position
        self.valor = glm.vec3(0,0,0)
        self.texture = Texture(texture_path)
    
    def set_posicao(self, x, y, z):
        self.valor[0] = x
        self.valor[1] = y
        self.valor[2] = z

    def get_posicao(self):
        return self.valor + self.position

    def update(self, velocidade):
        self.valor[0] -= velocidade


    def draw(self, x, y, z, tamanho):
        glPushMatrix()
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        glScale(1 * tamanho, 1 * tamanho, 1 * tamanho)
        glRotate(-90, 0, 1, 0)
        self.texture.bind()  
        glEnable(GL_TEXTURE_2D)

        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coords[i][j])  
                glVertex3fv(self.vertices[vertex])  
        glEnd()

        glDisable(GL_TEXTURE_2D)
        self.texture.unbind()  

        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y, 
                    self.position[2] + self.valor[2] + z)
        glTranslate(0,-15,0)
        glScale(0.5 * tamanho, 1 * tamanho, 1 * tamanho)
        glRotate(-90, 0, 0, 1)
        glRotate(90, 0, 1, 0)

        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            for j, vertex in enumerate(face):
                glTexCoord2f(*self.tex_coords[i][j]) 
                glVertex3fv(self.vertices[vertex])  
        glEnd()


        glPopMatrix()

        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glTranslatef(self.position[0] + self.valor[0] + x, 
                    self.position[1] + self.valor[1] + y - 35, 
                    self.position[2] + self.valor[2] + z)
        glScale(2, 40, 2)


        
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.facesC):
            for j, vertex in enumerate(face):
                glVertex3fv(self.verticesC[vertex]) 
        glEnd()


        glPopMatrix()

