import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

rotation_x = 0.0
rotation_y = 0.0


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


def render(vertices, faces):
    global rotation_x, rotation_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)

    glPushMatrix()

    
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)

    
    glScalef(1.0, 1.0, 1.0)  

    glBegin(GL_LINES)
    for face in faces:
        for i in range(len(face)):
            glVertex3fv(vertices[face[i]])
            glVertex3fv(vertices[face[(i + 1) % len(face)]])
    glEnd()

    glPopMatrix()

