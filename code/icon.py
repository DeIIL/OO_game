from settings import*

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        super().__init__(groups)
        self.icon = True

        #image
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = get_z_layers('main')

        self.rect = self.image.get_frect(center = pos)
        