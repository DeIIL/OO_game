from settings import *
from level import Level
from pytmx.util_pygame import load_pygame #to import tmx files for the map
from os.path import join #for relative paths for our especificy OS, cause the import path of the maptmx file can change
from support import *
class Game:
    def __init__(self):
        pygame.init()
        window_width, window_height = get_window_dimensions()
        self.__display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Super Pirate')
        self.__clock = pygame.Clock() #for measure the framerate 
        self.import_assets()

        self.__tmx_maps = {0: load_pygame(join('data', 'levels', 'omni.tmx'))}
        self.__current_stage = Level(self.__tmx_maps[0], self.__level_frames)

    def import_assets(self):
        self.__level_frames = {
            'flag': import_folder( 'graphics', 'level', 'flag' ),
            'saw': import_folder( 'graphics', 'enemies', 'saw', 'animation' ),
            'floor_spike': import_folder( 'graphics', 'enemies', 'floor_spikes' ),
            'palms': import_sub_folders( 'graphics', 'level', 'palms' ),
            'candle': import_folder( 'graphics', 'level', 'candle' ),
            'window': import_folder( 'graphics', 'level', 'big_chains' ),
            'big_chain': import_folder( 'graphics', 'level', 'big_chains' ),
            'small_chain': import_folder( 'graphics', 'level', 'small_chains' ),
            'candle_light': import_folder( 'graphics', 'level', 'candle light' ),
            'player': import_sub_folders( 'graphics', 'player' ),
            'saw': import_folder( 'graphics', 'enemies', 'saw', 'animation' ),
            'helicopter': import_folder( 'graphics', 'level', 'helicopter' ),
            'boat': import_folder( 'graphics', 'objects', 'boat' )
        }

    def run(self):
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
    game.run()