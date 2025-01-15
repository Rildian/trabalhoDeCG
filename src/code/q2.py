import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

rotation_x = 0.0
rotation_y = 0.0

# Função para carregar o modelo OBJ
def load_obj(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.strip().split()
                face = []
                for part in parts[1:]:
                    vertex_index = int(part.split('/')[0]) - 1
                    face.append(vertex_index)
                faces.append(face)

    return vertices, faces

# Função para centralizar e escalar os vértices
def center_and_scale(vertices):
    min_vals = [min(coord[i] for coord in vertices) for i in range(3)]
    max_vals = [max(coord[i] for coord in vertices) for i in range(3)]

    center = [(min_vals[i] + max_vals[i]) / 2.0 for i in range(3)]
    scale = max(max_vals[i] - min_vals[i] for i in range(3))

    for i in range(len(vertices)):
        vertices[i] = [(vertices[i][j] - center[j]) / scale for j in range(3)]

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def key_callback(window, key, scancode, action, mods):
    global rotation_x, rotation_y
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            rotation_x -= 10.0
        elif key == glfw.KEY_DOWN:
            rotation_x += 10.0
        elif key == glfw.KEY_LEFT:
            rotation_y -= 10.0
        elif key == glfw.KEY_RIGHT:
            rotation_y += 10.0

# Função para renderizar o modelo com escala ampliada
def render(vertices, faces):
    global rotation_x, rotation_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)

    glPushMatrix()

    # Aplicar rotações
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)

    # Ampliar a escala do modelo
    glScalef(1.0, 1.0, 1.0)  # Escala ampliada

    glBegin(GL_LINES)
    for face in faces:
        for i in range(len(face)):
            glVertex3fv(vertices[face[i]])
            glVertex3fv(vertices[face[(i + 1) % len(face)]])
    glEnd()

    glPopMatrix()

def main():
    
    obj_file_path = 'D:/trabalhoDeCG/src/objects/bike/moto_simple_2.obj'
    

    vertices, faces = load_obj(obj_file_path)
    center_and_scale(vertices)

    if not glfw.init():
        return

    janela = glfw.create_window(800, 600, 'Renderizador OBJ - Moto', None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, key_callback)

    init()

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        render(vertices, faces)
        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == '__main__':
    main()