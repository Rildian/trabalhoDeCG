import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from cubo import cubo_func
#from bike import draw_object, carregar_obj

# Configurações iniciais da câmera
def configure_camera():
    glLoadIdentity()
    gluLookAt(3.0, 3.0, 3.0, # pos
              0.0, 0.0, 0.0, # at
              0.0, 1.0, 0.0) # up


def initialize():
    glClearColor(0, 0, 0, 0)  
    glEnable(GL_DEPTH_TEST) 

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # adaptar a janela do dispositivo
    aspect_ratio = 800 / 600  
    if aspect_ratio >= 1.0:
        glOrtho(-3 * aspect_ratio, 3 * aspect_ratio, -3, 3, -5, 10)
    else:
        glOrtho(-5, 5, -5 / aspect_ratio, 10.0 / aspect_ratio, -15.0, 15.0)
    glMatrixMode(GL_MODELVIEW)


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    configure_camera()
    cubo_func()
    


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Trabalho de CG", None, None)
    
    if not window:
        glfw.terminate()
        print("Janela não foi criada por alguma razão.")
        return

    glfw.make_context_current(window)
    
    #arquivo = "D:\\trabalhoDeCG\\src\\objects\\bike\\bikee.obj"
    #vertices, faces, normais, texturas = carregar_obj(arquivo)


    icon = "icon.jpg"
    glfw.set_window_icon(window, 1, Image.open(icon))
    
    initialize()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
