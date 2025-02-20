import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from cubo import Cubo
from moto import Moto
from cenario import Cenario
from camera import Camera
from obstaculos import Obstaculos
import glm
from pyglm import *

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

def setup_callbacks(window, camera):
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

def process_input(camera):
    global cursor_disabled, esc_pressed, first_mouse
    camera.process_input(keys)
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        sergio.mover(0,0,0.1)
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        sergio.mover(0,0,-0.1)
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        sergio.mover(0.1,0,0)
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        sergio.mover(-0.1,0,0)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        moto.mover(-0.005)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        moto.mover(0.005)
    
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not esc_pressed:
        camera.toggle_cursor(window)
        esc_pressed = True
    elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
        esc_pressed = False

def render(camera):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera.update_view()
    #sergio.draw(0, 0, 0, 5)
    moto.draw()
    cenario.draw()
    obstaculo.draw()

def update():
    #sergio.update()
    moto.update()
    cenario.update()
    obstaculo.update()
    camera.set_position(moto.get_posicao()[0] - 20,moto.get_posicao()[1] + 10 ,moto.get_posicao()[2] )

def main():
    global window, keys, moto, sergio, cenario, camera, obstaculo
    
    width, height = 1000, 1000
    window = init_glfw(width, height, "Elf Stunden auf der Rennstrecke")
    init_opengl()
    load_texture("textura.png")
    
    keys = {}
    camera = Camera()
    setup_callbacks(window, camera)
    
    moto = Moto()
    #sergio = Cubo(texture_path="textura.png", initial_position=[-360, 0, 0])
    cenario = Cenario()
    obstaculo = Obstaculos(initial_position=glm.vec3(0.0, 0.0, 0.0)) 
    
    while not glfw.window_should_close(window):
        process_input(camera)
        render(camera)
        update()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == '__main__':
    main()
