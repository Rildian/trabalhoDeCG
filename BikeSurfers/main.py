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


class Game:
    def __init__(self, width=1000, height=1000, title="Elf Stunden auf der Rennstrecke"):
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self.keys = {}
        self.game_started = False
        self.pause_game = False
        self.colisao = False
        self.camera = Camera()

        self.init_window()
        self.init_opengl()
        self.setup_callbacks()

        self.moto = Moto()
        self.sergio = Cubo(texture_path="textura.png", initial_position=[-360, 0, 0])
        self.cenario = Cenario()
        self.obstaculo = Obstaculos()
        self.menu = Menu()

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
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            # Obtém o tamanho da janela
            width, height = glfw.get_window_size(self.window)
            
            # Calcula o centro da tela
            center_x, center_y = width // 2, height // 2

            center_y += 425
            
            # Obtém a posição do mouse
            mouse_x, mouse_y = glfw.get_cursor_pos(self.window)
            print(mouse_x)
            print(mouse_y)
            
            # Define uma margem de tolerância para o clique (exemplo: 50 pixels)
            tolerance_x = 150
            tolerance_y = 50
            

            # Verifica se o clique está dentro da área central
            if (center_x - tolerance_x <= mouse_x <= center_x + tolerance_x and 
                center_y - tolerance_y <= mouse_y <= center_y + tolerance_y):
                self.game_started = True  # Muda para o modo de jogo


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
            self.moto.mover(-0.005)
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.moto.mover(0.005)

    def bateu(self):
        motoPosicao = self.moto.get_posicao()
        
        for caminhao in self.obstaculo.caminhoes:  # Itera sobre a lista de caminhões
            caminhaoInicio, caminhaoFim = caminhao.get_trajeto()
            
            print(f" Rota: {caminhaoFim[2]}")
            print(f" Moto: {motoPosicao[2]}")
            print(f" Caminhao: {caminhao.valor[2] + caminhao.position[2]} ")
            
            pontoDeColisao = (motoPosicao[0] - caminhaoInicio[0]) / (caminhaoFim[0] - caminhaoInicio[0])
            
            if (self.obstaculo.get_p() - 0.02 <= pontoDeColisao <= self.obstaculo.get_p() + 0.02) \
                    and (caminhaoFim[2] - 8 <= motoPosicao[2] <= caminhaoFim[2] + 8):
                self.colisao = True
                print("Bateu")
                break  # Sai do loop ao detectar colisão


    def render_game(self, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update_view()
        self.moto.draw()
        self.obstaculo.draw()
        self.cenario.draw()

    def update_game(self):
        self.bateu()
        self.moto.update()
        self.cenario.update()
        self.obstaculo.update()
        self.camera.set_position(
            self.moto.get_posicao()[0] - 20,
            self.moto.get_posicao()[1] + 10,
            self.moto.get_posicao()[2],
        )

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Salva a matriz de projeção e muda para uma projeção ortográfica (2D)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  # Define uma projeção ortográfica
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self.menu.draw()  # Desenha o menu

        # Restaura as matrizes para a configuração anterior
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
            else:
                self.render_menu()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()


if __name__ == '__main__':
    Game().run()
