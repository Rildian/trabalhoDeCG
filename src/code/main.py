import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from q1 import load_obj, center_and_scale, render as render_moto
from PIL import Image


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



def render(vertices, faces):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    configure_camera()

    glTranslatef(moto_pos[0], moto_pos[1], moto_pos[2])
    render_moto(vertices, faces)
    


def main():
    global moto_pos

    # Carregar o modelo da moto
    obj_file_path = 'D:/trabalhoDeCG/src/objects/bike/moto_simple_2.obj'
    vertices, faces = load_obj(obj_file_path)
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

    initialize()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(vertices, faces)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
