from settings import *
import os
from level import Level
from pytmx.util_pygame import load_pygame #to import tmx files for the map
from os.path import join #for relative paths for our especificy OS, cause the import path of the maptmx file can change
from support import *
from menu import *
from main_menu import *
from continue_menu import *
from options_menu import *
from pygame import mixer

class Game:
    def __init__(self):
        pygame.init()
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.running = True
        self.playing = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False
        self.font_name = 'OO_game/Litebulb 8-bit.ttf'
        self.main_menu = MainMenu(self)
        self.continueM = ContinueMenu(self)
        self.options = OptionsMenu(self)
        self.current_menu = self.main_menu
        window_width, window_height = get_window_dimensions()
        self.window_width = window_width
        self.window_height = window_height 
        self.display = pygame.Surface((window_width, window_height))
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Super Pirate')
        self.__clock = pygame.Clock() #for measure the framerate 
        self.import_assets()

        script_dir = os.path.dirname(__file__)  
        self.__tmx_maps = {0: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', 'omni.tmx'))}
        self.__current_stage = Level(self.__tmx_maps[0], self.__level_frames)

    def import_assets(self):
        script_dir = os.path.dirname(__file__)
        self.__level_frames = {
            'flag': import_folder(script_dir, '..' , 'graphics', 'level', 'flag' ),
            'saw': import_folder( script_dir, '..' , 'graphics', 'enemies', 'saw', 'animation' ),
            'floor_spike': import_folder( script_dir, '..' , 'graphics', 'enemies', 'floor_spikes' ),
            'palms': import_sub_folders(script_dir, '..' ,  'graphics', 'level', 'palms' ),
            'candle': import_folder( script_dir, '..' , 'graphics', 'level', 'candle' ),
            'window': import_folder( script_dir, '..' , 'graphics', 'level', 'big_chains' ),
            'big_chain': import_folder( script_dir, '..' , 'graphics', 'level', 'big_chains' ),
            'small_chain': import_folder( script_dir, '..' , 'graphics', 'level', 'small_chains' ),
            'candle_light': import_folder( script_dir, '..' , 'graphics', 'level', 'candle light' ),
            'player': import_sub_folders( script_dir, '..' , 'graphics', 'player' ),
            'saw': import_folder(script_dir, '..' ,  'graphics', 'enemies', 'saw', 'animation' ),
            'helicopter': import_folder( script_dir, '..' , 'graphics', 'level', 'helicopter' ),
            'boat': import_folder(script_dir, '..' , 'graphics', 'objects', 'boat' )
        }

    def game_loop(self):
        window_width, window_height = get_window_dimensions()
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            pygame.display.update()
            self.reset_keys()

        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True                
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True                
                if event.key == pygame.K_UP:
                    self.UP_KEY = True


    def draw_text(self, text,size,x,y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)


    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False

    def run(self):
        dt = self.__clock.tick() / 100000
        mixer.music.stop()
        while True:
            dt = self.__clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.__current_stage.run(dt)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    ##game.run()
    while game.running:
        game.current_menu.display_menu()
        game.game_loop()