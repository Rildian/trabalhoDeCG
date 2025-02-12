from OpenGL.GL import *
import numpy as np

class Esfera:
    def __init__(self, inital_position=[0.0, 0.0, 0.0]):
        self.position = inital_position
        self.valor = [0, 0, 0]
        self.angulo = 0.0


    def update(self):
        self.angulo = (self.angulo + 0.01) % 360

    def mover(self, x, y, z):
        self.valor[0] += x
        self.valor[1] += y
        self.valor[2] += z

    def esfera(self, raio, slices, stacks):
        for i in range(stacks):
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
                glColor3f(j/slices, i/stacks, 1 - (i/stacks))
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()

    def draw(self, raio, slices, stacks, x, y, z):
        
        glPushMatrix()  
        glTranslatef(self.position[0] + self.valor[0] + x, self.position[1] + self.valor[1] + y,self.position[2] + self.valor[2] + z)
        glRotatef(15, 0, 0 ,1)
        glRotatef(-90, 1, 0 ,0)
        glRotatef(self.angulo, 0, 0 ,1)
        glRotatef(180, 0,1,0)
        self.esfera(raio, slices, stacks)
        glPopMatrix()