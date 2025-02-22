from OpenGL.GL import *
import glm

class Edicao:
    COLORS = {
        0: (0.5, 0.5, 0.5),   # Cinza
        1: (1.0, 0.3, 0.3),  # Vermelho
        2: (0.3, 1.0, 0.3),  # Verde
        3: (0.3, 0.3, 1.0) # Azul
    }

    vertices = [
        [-0.05, 0.05, 0],
        [0.05, 0.05, 0],
        [0.05, -0.05, 0],
        [-0.05, -0.05, 0] 
    ]
    
    def __init__(self, initial_position=glm.vec3(0.0, 0.0, 0.0)):
        self.position = initial_position
        self.grid_width = 16  # Número de colunas na grid
        self.grid_height = 3   # Número de linhas na grid
        self.square_size = 0.1  # Tamanho de cada quadrado
        self.spacing = 0.005    # Espaçamento entre os quadrados
        self.cor = 1
        self.matriz = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
        
        # Inicializa a grid com a cor cinza por padrão
        self.grid_colors = [[self.COLORS[0] for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def set_square_color(self, y, x, color_id):
        if color_id == 3  and x < 15:
            self.grid_colors[y][x] = self.COLORS[color_id]
            self.grid_colors[y][x+1] = self.COLORS[color_id]
            self.matriz[y][x] = color_id
        else:
            self.grid_colors[y][x] = self.COLORS[color_id]
            self.matriz[y][x] = color_id
        print(self.matriz[y])

    def set_cor(self,x):
        self.cor = x

    def get_cor(self):
        return self.cor

    def draw_square(self, x, y):
        glPushMatrix()

        # Calcula a posição do quadrado na grid
        glTranslatef(
            self.position.x + x * (self.square_size + self.spacing),
            self.position.y + y * (self.square_size + self.spacing),
            self.position.z
        )

        glDisable(GL_TEXTURE_2D)  
        glColor3f(*self.grid_colors[y][x])  # Define a cor baseada na grid

        glBegin(GL_QUADS)
        glVertex3f(-self.square_size / 2, self.square_size / 2, 0)  
        glVertex3f(self.square_size / 2, self.square_size / 2, 0)  
        glVertex3f(self.square_size / 2, -self.square_size / 2, 0) 
        glVertex3f(-self.square_size / 2, -self.square_size / 2, 0) 
        glEnd()
        
        glPopMatrix()

    def draw(self):
        total_width = self.grid_width * (self.square_size + self.spacing) - self.spacing
        total_height = self.grid_height * (self.square_size + self.spacing) - self.spacing

        self.position.x = -total_width / 2
        self.position.y = -total_height / 2

        for x in range(self.grid_width): 
            for y in range(self.grid_height):
                self.draw_square(x, y)
        
        glPushMatrix()
        glTranslatef(0, 0.3, 0) 

        glColor3f(1, 0.3, 0.3)

        glBegin(GL_QUADS)
        for i in range(4):
            glVertex3f(*self.vertices[i]) 
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.3, 0.3, 0) 

        glColor3f(0.3, 1, 0.3)

        glBegin(GL_QUADS)
        for i in range(4):
            glVertex3f(*self.vertices[i]) 
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.3, 0.3, 0) 

        glColor3f(0.3, 0.3, 1)

        glBegin(GL_QUADS)
        for i in range(4):
            glVertex3f(*self.vertices[i]) 
        glEnd()
        glPopMatrix()