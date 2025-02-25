import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

class Camera:
    def __init__(self, position=None, front=None, up=None):
        self.position = np.array(position if position else [-377.65, 20.68, 15.33])
        self.target_point = np.array([400.0, 0.0, 0.0])  
        self.up = np.array(up if up else [0.0, 1.0, 0.0])
        self.speed = 0.01
        self.yaw = -90.0
        self.pitch = 0.0
        self.sensitivity = 0.1
        self.first_mouse = True
        self.last_x, self.last_y = 500, 500
        self.cursor_disabled = False
        self.esc_pressed = False
        self.free_mode = False 
        self.front = self.calculate_fixed_front() 
        self.p = 0.5

    def calculate_fixed_front(self):
        direction = self.target_point - self.position
        return direction / np.linalg.norm(direction)

    def set_position(self, x, y, z):
        if not self.free_mode:
            self.position = np.array([x, y, z])
            self.front = self.calculate_fixed_front() 

    def update_view(self):
        glLoadIdentity()
        target = self.target_point if not self.free_mode else self.position + self.front * 2
        gluLookAt(*self.position, *target, *self.up)

    def process_input(self, keys):
        if self.free_mode:
            if keys.get(glfw.KEY_W, False):
                self.position += self.speed * self.front
            if keys.get(glfw.KEY_S, False):
                self.position -= self.speed * self.front
            if keys.get(glfw.KEY_A, False):
                self.position -= np.cross(self.front, self.up) * self.speed
            if keys.get(glfw.KEY_D, False):
                self.position += np.cross(self.front, self.up) * self.speed
            self.speed = 0.1 if keys.get(glfw.KEY_LEFT_SHIFT, False) else 0.01

            


    def mouse_callback(self, window, xpos, ypos):
        if not self.free_mode:
            return

        if self.first_mouse:
            self.last_x, self.last_y = xpos, ypos
            self.first_mouse = False

        xoffset = (xpos - self.last_x) * self.sensitivity
        yoffset = (self.last_y - ypos) * self.sensitivity
        self.last_x, self.last_y = xpos, ypos

        self.yaw += xoffset
        self.pitch = max(min(self.pitch + yoffset, 89.0), -89.0)

        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.front = direction / np.linalg.norm(direction)

    def toggle_cursor(self, window):
        self.free_mode = not self.free_mode
        mode = glfw.CURSOR_DISABLED if self.free_mode else glfw.CURSOR_NORMAL
        glfw.set_input_mode(window, glfw.CURSOR, mode)
        self.first_mouse = self.free_mode

        if not self.free_mode:
            self.front = self.calculate_fixed_front()
