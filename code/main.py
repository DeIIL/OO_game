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
from data import Data
from debug import debug
from ui import UI   
from overworld import Overworld

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
        self.ui = UI(self.font_name, self.ui_frames)
        self.data = Data(self.ui)
        self.__tmx_maps = {
            0: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '0.tmx')),
            1: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '1.tmx')),
            2: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '2.tmx')),
            3: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '3.tmx')),
            4: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '4.tmx')),
            5: load_pygame(os.path.join(script_dir, '..', 'data', 'levels', '5.tmx')),}
        self.tmx_overworld = load_pygame(os.path.join(script_dir, '..', 'data', 'overworld', 'overworld.tmx'))
        self.__current_stage = Level(self.__tmx_maps[self.data.current_level], self.__level_frames,self.audio_files, self.data, self.switch_stage)
        
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.__current_stage = Level(self.__tmx_maps[self.data.current_level], self.__level_frames,self.audio_files, self.data, self.switch_stage)
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.__current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

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
            'saw_chain': import_image(script_dir, '..' ,   'graphics', 'enemies', 'saw', 'saw_chain' ),
            'helicopter': import_folder( script_dir, '..' , 'graphics', 'level', 'helicopter' ),
            'boat': import_folder(script_dir, '..' , 'graphics', 'objects', 'boat' ),
            'spike': import_image(script_dir, '..' ,  'graphics', 'enemies', 'spike_ball', 'Spiked Ball' ),
            'spike_chain': import_image(script_dir, '..' ,  'graphics', 'enemies', 'spike_ball', 'spiked_chain' ),
            'tooth': import_folder(script_dir, '..' ,  'graphics', 'enemies', 'tooth', 'run' ),
            'shell': import_sub_folders(script_dir, '..' ,  'graphics', 'enemies', 'shell' ),
            'pearl': import_image(script_dir, '..' ,  'graphics', 'enemies', 'bullets', 'pearl' ),
            'items': import_sub_folders (script_dir, '..' , 'graphics' , 'items'),
            'particle': import_folder(script_dir, '..' , 'graphics' , 'effects', 'particle'),
            'water_top': import_folder( script_dir, '..' , 'graphics', 'level', 'water', 'top' ),
            'water_body': import_image( script_dir, '..' , 'graphics', 'level', 'water', 'body' ),
            'bg_tiles': import_folder_dict(script_dir, '..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder(script_dir,'..', 'graphics','level', 'clouds', 'small'),
			'cloud_large': import_image(script_dir, '..', 'graphics','level', 'clouds', 'large_cloud')	
        }

        self.ui_frames = {
            'heart': import_folder(script_dir, '..', 'graphics' , 'ui' , 'heart'),
            'coin': import_image(script_dir, '..', 'graphics' , 'ui' , 'coin')
        }

        self.overworld_frames = {
            'palms': import_folder(script_dir, '..', 'graphics' , 'overworld' , 'palm'),
            'water': import_folder(script_dir, '..', 'graphics' , 'overworld' , 'water'),   
            'path': import_folder_dict(script_dir, '..', 'graphics' , 'overworld' , 'path'),
            'icon': import_sub_folders(script_dir, '..', 'graphics' , 'overworld' , 'icon'),  
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join(script_dir, '..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join(script_dir,'..', 'audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join(script_dir,'..', 'audio', 'jump.wav')), 
			'damage': pygame.mixer.Sound(join(script_dir,'..', 'audio', 'damage.wav')),
			'pearl': pygame.mixer.Sound(join(script_dir,'..', 'audio', 'pearl.wav')),
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

    def check_game_over(self):
        if self.data.health < 0:
            pygame.quit()

    def run(self):
        dt = self.__clock.tick() / 100000
        mixer.music.stop()
        while True:
            dt = self.__clock.tick() / 600
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.check_game_over()
            self.__current_stage.run(dt)
            self.ui.update(dt)
            pygame.display.update()
 
if __name__ == '__main__':
    game = Game()
    ##game.run()
    while game.running:
        game.current_menu.display_menu()
        game.game_loop()