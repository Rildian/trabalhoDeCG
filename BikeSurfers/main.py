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
from terra import Terra
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
    glFrustum(-1, 1, -1, 1, 1, 2000)
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

def ajustar_valor(valor: int, ajuste: int) -> int:
    novo_valor = valor + ajuste
    return max(0, min(2, novo_valor))

def ajustar_posicao(valor: int):
    global posicao
    if posicao == 0:
        if valor > 0:
            posicao += 1
            moto.mover(0,0,16.6)
    elif posicao == 2:
        if valor < 0:
            posicao -= 1
            moto.mover(0,0,-16.6)
    elif posicao == 1:
        if valor > 0:
            posicao = ajustar_valor(posicao, valor)
            moto.mover(0,0,16.6)
        else:
            posicao = ajustar_valor(posicao, valor)
            moto.mover(0,0,-16.6)
        
        


def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    target = camera_pos + camera_front * 2
    gluLookAt(*camera_pos, *target, *camera_up)
    print(camera_pos)
    print(camera_front)

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
        if key == glfw.KEY_LEFT:
            ajustar_posicao(-1)
        elif key == glfw.KEY_RIGHT:
            ajustar_posicao(1)
    elif action == glfw.RELEASE:
        keys[key] = False

def process_input():
    global camera_pos, camera_front, camera_up, camera_speed, cursor_disabled, esc_pressed, first_mouse, posicao

    if keys.get(glfw.KEY_W, False):
        camera_pos += camera_speed * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= camera_speed * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_UP, False):
        sergio.mover(0.1,0,0)
    if keys.get(glfw.KEY_DOWN, False):
        sergio.mover(-0.1,0,0)
    if keys.get(glfw.KEY_LEFT, False):
        sergio.mover(0,0,-0.1)
    if keys.get(glfw.KEY_RIGHT, False):
        sergio.mover(0,0,0.1)
    #if keys.get(glfw.KEY_UP, False):
        #moto.mover(0.1, 0.0, 0.0)
    #if keys.get(glfw.KEY_DOWN, False):
        #moto.mover(-0.1, 0.0, 0.0)
    if keys.get(glfw.KEY_SPACE, False):
        moto.mover(0.0, 0.0, 0.0)
    
    camera_speed = 0.1 if keys.get(glfw.KEY_LEFT_SHIFT, False) else 0.01
    
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not esc_pressed:
        cursor_disabled = not cursor_disabled
        mode = glfw.CURSOR_DISABLED if cursor_disabled else glfw.CURSOR_NORMAL
        glfw.set_input_mode(window, glfw.CURSOR, mode)
        esc_pressed = True
        first_mouse = cursor_disabled
    elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
        esc_pressed = False

def floor_loop():
    global pos, pos2
    print(pos)
    print(pos2)
    pos[0] -= chao.get_aceleracao()
    pos2[0] -= chao2.get_aceleracao()
    if pos[0] == -1600:
        chao.set_posicao(800, 0, 0)
        terra.set_posicao(800,0,0)
        pos[0] = 0
    if pos2[0] == -1600:
        chao2.set_posicao(0, 0, 0)
        terra1.set_posicao(0,0,0)
        pos2[0] = 0

        

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
    sergio.draw(0, 0, 0, 5)
    moto.draw()
    chao.draw(0 ,0, 0)
    chao2.draw(800 ,0, 0)
    ceu.draw(0,0,0,800)
    terra.draw(0,398,0)
    terra1.draw(800,398,0)

def update():
    sergio.update()
    planet.update()
    moto.roda.update()
    chao.update()
    chao2.update()
    terra1.update()
    terra.update()
    floor_loop()

def main():
    global window, camera_pos, camera_front, camera_up, camera_speed, yaw, pitch
    global first_mouse, cursor_disabled, esc_pressed, sensitivity, last_x, last_y
    global planet, sergio, moto, keys, chao, chao2, ceu, posicao, pos, pos2, terra, terra1
    
    width, height = 1000,1000
    window = init_glfw(width, height, "Elf Stunden auf der Rennstrecke")
    init_opengl()
    load_texture("textura.png")
    setup_callbacks(window)


    keys = {}
    camera_pos = np.array([-23.97089551,  21.73997613,  15.72847116])
    camera_front = np.array([ 0.62827279, -0.64278761, -0.43828917])
    camera_up = np.array([0.0, 1.0, 0.0])
    camera_speed, yaw, pitch = 0.01, -90, 0.0
    first_mouse, cursor_disabled, esc_pressed = True, False, False
    sensitivity, last_x, last_y = 0.1, width / 2, height / 2
    posicao = 1
    
    pos = [-800,0,0]
    pos2 = [0,0,0]
    planet = Esfera()
    moto = Moto()
    terra = Terra(texture_path = "skybox.png")
    terra1 = Terra(texture_path = "skybox.png")
    sergio = Cubo(texture_path = "textura.png")
    chao = Chao(texture_path = "asfalto.jpg")
    chao2 = Chao(texture_path = "asfalto.jpg")
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