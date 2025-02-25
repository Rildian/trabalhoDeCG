import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from cubo import Cubo
from moto import Moto
from cenario import Cenario
from camera import Camera
from menu import Menu
from obstaculos import Obstaculos
from edicao import Edicao
from derrota import Derrota
from text_display import TextDisplay

class Game:
    def __init__(self, width=1000, height=1000, title="Elf Stunden auf der Rennstrecke"):
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self.keys = {}
        self.game_started = False
        self.edicao_started = False 
        self.pause_game = False
        self.colisao = False
        self.derrotado = False
        self.camera = Camera()

        self.init_window()
        self.init_opengl()
        self.setup_callbacks()
        self.moto = Moto()
        self.sergio = Cubo(texture_path="textura.png", initial_position=[-360, 0, 0])
        self.cenario = Cenario()
        self.obstaculo = Obstaculos()
        self.menu = Menu()
        self.edicao = Edicao()
        self.derrota = Derrota()
        self.text_display = TextDisplay(width, height)
        self.pontos = 0

    def init_window(self):
        if not glfw.init():
            raise Exception("Falha ao iniciar GLFW")

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Não foi possível criar a janela!")

        glfw.make_context_current(self.window)

    def init_opengl(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glClearColor(1, 1, 1, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1, 1, -1, 1, 1, 1000)
        glMatrixMode(GL_MODELVIEW)

    def load_texture(self, image_path):
        image = Image.open(image_path)
        glfw.set_window_icon(self.window, 1, image)

    def setup_callbacks(self):
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.camera.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
            if self.game_started:
                if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                    self.camera.toggle_cursor(self.window)
                if glfw.get_key(self.window, glfw.KEY_TAB) == glfw.PRESS:
                    if self.pause_game:
                        self.pause_game = False
                    else:
                        self.pause_game = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def mouse_button_callback(self, window, button, action, mods):
        if not self.game_started and not self.edicao_started:
            if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
                width, height = glfw.get_window_size(self.window)
                
                center_x, center_y = width // 2, height // 2
                center_y += 425
                
                mouse_x, mouse_y = glfw.get_cursor_pos(self.window)

                tolerance_x = 150
                tolerance_y = 50
                
                if (center_x - tolerance_x <= mouse_x <= center_x + tolerance_x and 
                    center_y - tolerance_y <= mouse_y <= center_y + tolerance_y):
                    self.edicao_started = True 

        elif self.edicao_started:
            if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
                width, height = glfw.get_window_size(self.window)

                mouse_x, mouse_y = glfw.get_cursor_pos(self.window)
                
                grid_x_start, grid_y_start = 56, 600
                grid_x_end, grid_y_end = 900, 450
                
                cell_width = (grid_x_end - grid_x_start) / 16
                cell_height = (grid_y_start - grid_y_end) / 3

                tolerancia = 25
                
                tolerancia_x = 125
                tolerancia_y = 25
                
                if grid_x_start <= mouse_x <= grid_x_end and grid_y_end <= mouse_y <= grid_y_start:
                    x = int((mouse_x - grid_x_start) / cell_width)
                    y = int((grid_y_start - mouse_y) / cell_height)
                    
                    if self.edicao.get_cor() == self.edicao.matriz[y][x]:
                        if self.edicao.matriz[y][x] == 3:
                            self.edicao.set_square_color(y, x, 0)
                            self.edicao.set_square_color(y, x+1, 0)
                        else:
                            self.edicao.set_square_color(y, x, 0)
                    elif not self.edicao.matriz[y][x-1] == 3 and self.edicao.matriz[y][x] == 0 and not (self.edicao.get_cor() == 3 and self.edicao.matriz[y][x+1] != 0):
                        self.edicao.set_square_color(y, x, self.edicao.get_cor())

                if  500 - tolerancia_x <= mouse_x <= 500 + tolerancia_x and 750 - tolerancia_y <= mouse_y <= 750 + tolerancia_y and self.edicao.check_matriz():
                    self.pontos = 0
                    self.obstaculo.set_matriz(self.edicao.matriz)
                    self.obstaculo.set_obstaculos()
                    self.game_started = True

                if  500 - tolerancia <= mouse_x <= 500 + tolerancia and 350 - tolerancia <= mouse_y <= 350 + tolerancia:
                    self.edicao.set_cor(1)

                if  350 - tolerancia <= mouse_x <= 350 + tolerancia and 350 - tolerancia <= mouse_y <= 350 + tolerancia:
                    self.edicao.set_cor(3)

                if  650 - tolerancia <= mouse_x <= 650 + tolerancia and 350 - tolerancia <= mouse_y <= 350 + tolerancia:
                    self.edicao.set_cor(2)

                    

                

    def process_input(self):
        self.camera.process_input(self.keys)
        
        if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.sergio.mover(0, 0, 0.1)
        if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
            self.sergio.mover(0, 0, -0.1)
        if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
            self.sergio.mover(0.1, 0, 0)
        if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
            self.sergio.mover(-0.1, 0, 0)
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.moto.mover(-0.01)
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.moto.mover(0.01)

    def bateu(self):
        motoPosicao = self.moto.get_posicao()
        
        if len(self.obstaculo.caminhoes) > 0:
            for caminhao in self.obstaculo.caminhoes: 
                caminhaoInicio, caminhaoFim = caminhao.get_trajeto()
                
                pontoDeColisao = (motoPosicao[0] - caminhaoInicio[0]) / (caminhaoFim[0] - caminhaoInicio[0])
                
                if (self.obstaculo.get_p() - 0.02 <= pontoDeColisao <= self.obstaculo.get_p() + 0.02) \
                        and (caminhaoFim[2] - 10 <= motoPosicao[2] <= caminhaoFim[2] + 10):
                    self.derrotado = True
                    self.game_started = False
                    self.edicao_started = False
                    print("Bateu")
        
        if len(self.obstaculo.motos) > 0:
            for moto in self.obstaculo.motos: 
                motoInicio, motoFim = moto.get_trajeto()
                
                pontoDeColisao = (motoPosicao[0] - motoInicio[0]) / (motoFim[0] - motoInicio[0])
                
                if (self.obstaculo.get_p() - 0.01 <= pontoDeColisao <= self.obstaculo.get_p() + 0.01) \
                        and (motoFim[2] - 2 <= motoPosicao[2] <= motoFim[2] + 2):
                    self.derrotado = True
                    self.game_started = False
                    self.edicao_started = False
                    print("Bateu")
        
        if len(self.obstaculo.carros) > 0:
            for carro in self.obstaculo.carros: 
                carroInicio, carroFim = carro.get_trajeto()
                
                pontoDeColisao = (motoPosicao[0] - carroInicio[0]) / (carroFim[0] - carroInicio[0])
                
                if (self.obstaculo.get_p() - 0.013 <= pontoDeColisao <= self.obstaculo.get_p() + 0.013) \
                        and (carroFim[2] - 8 <= motoPosicao[2] <= carroFim[2] + 8):
                    self.derrotado = True
                    self.game_started = False
                    self.edicao_started = False
                    print("Bateu")


    def render_game(self, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update_view()
        self.moto.draw()
        self.obstaculo.draw()
        self.cenario.draw()
        self.text_display.render(f"Pontos: {self.pontos}")

    def update_game(self):
        self.moto.update()
        self.cenario.update()
        self.obstaculo.update()
        self.pontos += 1 
        self.camera.set_position(
            self.moto.get_posicao()[0] - 20,
            self.moto.get_posicao()[1] + 10,
            self.moto.get_posicao()[2],
        )
        self.bateu()

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self.menu.draw()  

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def render_fim(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1) 
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self.derrota.draw() 

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def render_edicao(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self.edicao.draw() 

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)




    def run(self):
        while not glfw.window_should_close(self.window):
            self.process_input()
            if self.game_started:
                self.render_game(self.camera)
                if not self.pause_game and not self.colisao:
                    self.update_game()
            elif self.edicao_started:
                self.render_edicao()
            elif self.derrotado:
                self.render_fim()
            else:
                self.render_menu()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()


if __name__ == '__main__':
    Game().run()
