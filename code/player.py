from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        self.__image = pygame.Surface((48, 56))
        self.__image.fill('red')

        # rects
        self.__rect = self.__image.get_frect(topleft=position)
        self.__old_rect = self.__rect.copy()

        # movement
        self.__direction = vector()  # vector which came from alas in settings.py ps:no parameters passed means de directions are 0
        self.__speed = 200
        self.__gravity = 1300
        self.__jump = False
        self.__jump_height = 500

        # collision
        self.__collision_sprites = collision_sprites
        self.__on_surface = {'floor': False, 'left': False, 'right': False}

    # Property getters for accessing private attributes
    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect
    
    @property
    def old_rect(self):
        return self.__old_rect
    
    # Property setters for modifying private attributes
    @image.setter
    def image(self, value):
        self.__image = value
    
    @rect.setter
    def rect(self, value):
        self.__rect = value
    
    @old_rect.setter
    def old_rect(self, value):
        self.__old_rect = value

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)  # vector for if for example both right and left keys are pressed in the same frame they subtraction each other
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_d]:
            input_vector.x += 1
        self.__direction.x = input_vector.normalize().x if input_vector else input_vector.x  # length of the vector always be 1

        if keys[pygame.K_SPACE]:
            self.__jump = True

    def move(self, dt):
        # horizontal
        self.__rect.x += self.__direction.x * self.__speed * dt
        self.__collision('horizontal')
        # vertical
        self.__direction.y += self.__gravity / 2 * dt
        self.__rect.y += self.__direction.y * dt
        self.__direction.y += self.__gravity / 2 * dt
        self.__collision('vertical')

        if self.__jump:
            if self.__on_surface['floor']:
                self.__direction.y = -self.__jump_height
            self.__jump = False

    def check_contact(self):
        floor_rect = pygame.Rect(self.__rect.bottomleft, (self.__rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.__collision_sprites]
        
        # collisions
        self.__on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def __collision(self, axis):
        for sprite in self.__collision_sprites:
            if sprite.rect.colliderect(self.__rect):
                if axis == 'horizontal':
                    # left
                    if self.__rect.left <= sprite.rect.right and self.__old_rect.left >= sprite.old_rect.right:
                        self.__rect.left = sprite.rect.right
                    # right
                    if self.__rect.right >= sprite.rect.left and self.__old_rect.right <= sprite.old_rect.left:
                        self.__rect.right = sprite.rect.left
                else:
                    # top
                    if self.__rect.top <= sprite.rect.bottom and self.__old_rect.top >= sprite.old_rect.bottom:
                        self.__rect.top = sprite.rect.bottom
                    # bottom
                    if self.__rect.bottom >= sprite.rect.top and self.__old_rect.bottom <= sprite.old_rect.top:
                        self.__rect.bottom = sprite.rect.top
                    self.__direction.y = 0

    def update(self, dt):
        self.__old_rect = self.__rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()