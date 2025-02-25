import pygame
import time
from OpenGL.GL import *
from OpenGL.GLU import *

class TextDisplay:
    def __init__(self, width=800, height=600):
        pygame.font.init()
        self.width = width
        self.height = height
        self.start_time = time.time()
        self.font = pygame.font.SysFont("Arial", 36)
        self.text_color = (255, 255, 0)    
        self.bg_color = (0, 0, 0, 0)    

    def get_points(self):
        """Retorna os pontos baseados no tempo decorrido"""
        return int(time.time() - self.start_time)

    def render(self, text="Pontos: 0"):
        """Renderiza texto na posição especificada"""
        points = self.get_points()
        text_to_show = f"Pontos: {points}" if text is None else text
        
        text_surface = self.font.render(text, True, self.text_color, self.bg_color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        w, h = text_surface.get_size()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glRasterPos2f(20, 100)
        glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def reset_timer(self):
        self.start_time = time.time()