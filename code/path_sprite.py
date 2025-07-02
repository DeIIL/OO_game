from settings import*
from sprites import Sprite

class PathSprite(Sprite):
    def __init__(self,pos,surf,group,level):
        super().__init__(pos,surf,group, get_z_layers('path'))
        self.level = level