import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from moto import load_obj, center_and_scale, render as render_moto
from PIL import Image
import os


moto_pos = [1.0, 1.0, 1.0]

def configure_camera():
    glLoadIdentity()
    gluLookAt(3.0, 3.0, 3.0,  # posição da câmera
              0.0, 0.0, 0.0,  # ponto focal
              0.0, 1.0, 0.0)  # vetor "up"

def initialize():
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    aspect_ratio = 800 / 600
    if aspect_ratio >= 1.0:
        glOrtho(-1 * aspect_ratio, 1 * aspect_ratio, -1, 1, -5, 10)
    else:
        glOrtho(-5, 5, -5 / aspect_ratio, 10.0 / aspect_ratio, -15.0, 15.0)
    glMatrixMode(GL_MODELVIEW)

def key_callback(window, key, scancode, action, mods):
    global moto_pos

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:  
            moto_pos[1] += 0.1
        elif key == glfw.KEY_DOWN:  
            moto_pos[1] -= 0.1
        elif key == glfw.KEY_LEFT:  
            moto_pos[0] -= 0.1
        elif key == glfw.KEY_RIGHT:  
            moto_pos[0] += 0.1
        elif key == glfw.KEY_W:  
            moto_pos[2] -= 0.1
        elif key == glfw.KEY_S:  
            moto_pos[2] += 0.1

def render(vertices, faces):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    configure_camera()

    glTranslatef(moto_pos[0], moto_pos[1], moto_pos[2])
    render_moto(vertices, faces)
    


def main():
    global moto_pos

    # Carregar o modelo da moto, usando path absoluto
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bike_obj_file_path = os.path.join(script_dir, 'bike_object.obj')

    vertices, faces = load_obj(bike_obj_file_path)
    center_and_scale(vertices)

    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return

    window = glfw.create_window(800, 600, "Trabalho de CG", None, None)
    icon = "icon.jpg"
    glfw.set_window_icon(window, 1, Image.open(icon))

    if not window:
        glfw.terminate()
        print("Janela não foi criada por alguma razão.")
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    initialize()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(vertices, faces)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
