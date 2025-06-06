from settings import *
from level import Level
from pytmx.util_pygame import load_pygame #to import tmx files for the map
from os.path import join #for relative paths for our especificy OS, cause the import path of the maptmx file can change

class Game:
    def __init__(self):
        pygame.init()
        window_width, window_height = get_window_dimensions()
        self.__display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('SuperTest')
        self.__clock = pygame.Clock() #for measure the framerate 

        self.__tmx_maps = {0: load_pygame(join('data', 'levels', 'omni.tmx'))}
        self.__current_stage = Level(self.__tmx_maps[0])

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