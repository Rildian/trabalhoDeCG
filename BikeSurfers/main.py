import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from esfera import Esfera
from cubo import Cubo
from moto import Moto
from chao import Chao
from ceu import Ceu
import os

moto = None


def init_glfw(width, height, title):
    if not glfw.init():
        raise Exception("Falha ao iniciar GLFW")
    
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Não foi possível criar a janela!")
    
    glfw.make_context_current(window)
    return window

def init_opengl():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 1000)
    glMatrixMode(GL_MODELVIEW)


def load_texture(image_path):
    image = Image.open(image_path)
    glfw.set_window_icon(window, 1, image)

def setup_callbacks(window):
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)

def circulo(x, y, raio, segments):
    glColor3f(0, 1, 1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = 2 * np.pi * i/segments
        glVertex2f(x + np.cos(angle) * raio, y + np.sin(angle) * raio)
    glEnd()


def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    target = camera_pos + camera_front * 2
    gluLookAt(*camera_pos, *target, *camera_up)

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def process_input():
    global camera_pos, camera_front, camera_up, camera_speed, cursor_disabled, esc_pressed, first_mouse

    if keys.get(glfw.KEY_W, False):
        camera_pos += camera_speed * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= camera_speed * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_UP, False):
        moto.mover(0.0, 0.0, 0.1)
    if keys.get(glfw.KEY_DOWN, False):
        moto.mover(0.0, 0.0, -0.1)
    if keys.get(glfw.KEY_LEFT, False):
        moto.mover(-0.1, 0.0, 0.0)
    if keys.get(glfw.KEY_RIGHT, False):
        moto.mover(0.1, 0.0, 0.0)
    if keys.get(glfw.KEY_SPACE, False):
        moto.mover(0.0, 0.0, 0.0)
    
    camera_speed = 0.05 if keys.get(glfw.KEY_LEFT_SHIFT, False) else 0.01
    
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not esc_pressed:
        cursor_disabled = not cursor_disabled
        mode = glfw.CURSOR_DISABLED if cursor_disabled else glfw.CURSOR_NORMAL
        glfw.set_input_mode(window, glfw.CURSOR, mode)
        esc_pressed = True
        first_mouse = cursor_disabled
    elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
        esc_pressed = False

def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse, camera_front, cursor_disabled, sensitivity
    
    if not cursor_disabled:
        return
    
    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False
    
    xoffset, yoffset = (xpos - last_x) * sensitivity, (last_y - ypos) * sensitivity
    last_x, last_y = xpos, ypos
    
    yaw, pitch = yaw + xoffset, max(min(pitch + yoffset, 89.0), -89.0)
    
    direction = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    camera_front[:] = direction / np.linalg.norm(direction)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera()
    #planet.draw(5, 10, 10, 5, 5, -5)
    #planet.draw(5, 10, 10, 0, 0, 0)
    sergio.draw(-10, 5, -10, 5)
    moto.draw()
    chao.draw()
    ceu.draw(0,0,0,800)

def update():
    sergio.update()
    planet.update()
    moto.roda.update()

def main():
    global window, camera_pos, camera_front, camera_up, camera_speed, yaw, pitch
    global first_mouse, cursor_disabled, esc_pressed, sensitivity, last_x, last_y
    global planet, sergio, moto, keys, chao, ceu
    
    width, height = 800, 800
    window = init_glfw(width, height, "Teste OpenGL")
    init_opengl()
    load_texture("textura.png")
    setup_callbacks(window)


    keys = {}
    camera_pos = np.array([0.0, 0.0, 10])
    camera_front = np.array([0.0, 0.0, -1.0])
    camera_up = np.array([0.0, 1.0, 0.0])
    camera_speed, yaw, pitch = 0.01, -90, 0.0
    first_mouse, cursor_disabled, esc_pressed = True, False, False
    sensitivity, last_x, last_y = 0.1, width / 2, height / 2
    
    planet = Esfera()
    moto = Moto()
    sergio = Cubo(texture_path = "textura.png")
    chao = Chao()
    ceu = Ceu(texture_path = "skybox.png")
    
    while not glfw.window_should_close(window):
        process_input()
        render()
        update()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == '__main__':
    main()