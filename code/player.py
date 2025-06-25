from settings import *
from timer import Timer
from os.path import join #for relative paths for our especificy OS, cause the import path of the maptmx file can change

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, semi_collision_sprites, frame):
        super().__init__(groups)
        self.__z = get_z_layers('main')
        
        #image
        self.__frames, self.__frame_index = frame, 0
        self.__state, self.__facing_right = 'idle', True
        self.__image = self.__frames[self.__state][self.__frame_index]

        # rects
        self.__rect = self.__image.get_frect(topleft=position)
        self.__hitbox_rect = self.__rect.inflate(-76, -36)
        self.__old_rect = self.__hitbox_rect.copy()

        # movement
        self.__direction = vector()  # vector which came from alas in settings.py ps:no parameters passed means de directions are 0
        self.__speed = 200
        self.__gravity = 1300
        self.__jump = False
        self.__jump_height = 900
        self.__attacking = False

        # collision
        self.__collision_sprites = collision_sprites
        self.__semi_collision_sprites = semi_collision_sprites
        self.__on_surface = {'floor': False, 'left': False, 'right': False}
        self.__platform = None

        #timer
        self.timers = {
            'wall jump': Timer(250),
            'wall slide block': Timer(250),
            'platform skip': Timer(100),
            'attack cd': Timer(500)
        }

    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect
    
    @property
    def old_rect(self):
        return self.__old_rect
    
    @property
    def hitbox_rect(self):
        return self.__hitbox_rect
    
    @property
    def z(self):
        return self.__z
    
    @image.setter
    def image(self, value):
        self.__image = value
    
    @rect.setter
    def rect(self, value):
        self.__rect = value
    
    @old_rect.setter
    def old_rect(self, value):
        self.__old_rect = value

    @hitbox_rect.setter
    def hitbox_rect(self, value):
        self.__hitbox_rect = value

    @z.setter
    def z(self, value):
        self.__z = value

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)  # vector for if for example both right and left keys are pressed in the same frame they subtraction each other
        if not self.timers['wall jump'].active:
            #move left
            if keys[pygame.K_a]:
                input_vector.x -= 1
                self.__facing_right = False
            #move right
            if keys[pygame.K_d]:
                input_vector.x += 1
                self.__facing_right = True
            #go down the platform
            if keys[pygame.K_s]:
                self.timers['platform skip'].activate()
            #attack
            if keys[pygame.K_j]:
                self.attack()

            self.__direction.x = input_vector.normalize().x if input_vector else input_vector.x  # length of the vector always be 1

        if keys[pygame.K_SPACE]:
            self.__jump = True

    def attack(self):
        if not self.timers['attack cd'].active:
            self.__attacking = True
            self.__frame_index = 0
            self.timers['attack cd'].activate()

    def move(self, dt):
        # horizontal
        self.__hitbox_rect.x += self.__direction.x * self.__speed * dt
        self.__collision('horizontal')
        # vertical
        if not self.__on_surface['floor'] and any((self.__on_surface['left'], self.__on_surface['right'])) and not self.timers['wall slide block'].active: #
            self.__direction.y = 0 #stops any existing fall or jumping mechanic
            self.__hitbox_rect.y += self.__gravity / 10 * dt
        else:
            self.__direction.y += self.__gravity / 2 * dt
            self.__hitbox_rect.y += self.__direction.y * dt
            self.__direction.y += self.__gravity / 2 * dt

        if self.__jump:
            if self.__on_surface['floor']:
                self.__direction.y = -self.__jump_height
                self.timers['wall slide block'].activate()
                self.__hitbox_rect.bottom -= 1
            elif any((self.__on_surface['left'], self.__on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.__direction.y = -self.__jump_height
                self.__direction.x = 1 if self.__on_surface['left'] else -1 #MAKE ALWAYS JUMP THE OPOSITIVE DIRECTION OF THE WALL
            self.__jump = False 

        self.__collision('vertical')
        self.semi_collision()
        self.__rect.center = self.__hitbox_rect.center
    
    def platform_move(self, dt):
        if self.__platform:
            self.__hitbox_rect.topleft += self.__platform.direction * self.__platform.speed * dt #if player is stading in the platform move the player in the direction of the platform with the same speed * the bitframerate

    def check_contact(self):
        floor_rect = pygame.Rect(self.__hitbox_rect.bottomleft, (self.__hitbox_rect.width, 2))#left,top,width,height
        right_rect = pygame.Rect(self.__hitbox_rect.topright + vector(0, self.__hitbox_rect.height / 4), (2, (self.__hitbox_rect.height) / 2))
        left_rect = pygame.Rect(self.__hitbox_rect.topleft + vector(-2, self.__hitbox_rect.height / 4), (2, (self.__hitbox_rect.height) / 2))
        collide_rects = [sprite.rect for sprite in self.__collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.__semi_collision_sprites]
        
        # collisions
        self.__on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.__direction.y >= 0 else False
        self.__on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.__on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        #standing in move platform
        self.__platform = None
        sprites = self.__collision_sprites.sprites() + self.__semi_collision_sprites.sprites() #.sprites in a group gives us a list
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.__platform = sprite

    def __collision(self, axis):
        for sprite in self.__collision_sprites:
            if sprite.rect.colliderect(self.__hitbox_rect):
                if axis == 'horizontal':
                    # left
                    if self.__hitbox_rect.left <= sprite.rect.right and int(self.__old_rect.left) >= int(sprite.old_rect.right):
                        self.__hitbox_rect.left = sprite.rect.right
                    # right
                    if self.__hitbox_rect.right >= sprite.rect.left and int(self.__old_rect.right) <= int(sprite.old_rect.left):
                        self.__hitbox_rect.right = sprite.rect.left
                else:
                    # top
                    if self.__hitbox_rect.top <= sprite.rect.bottom and int(self.__old_rect.top) >= int(sprite.old_rect.bottom):
                        self.__hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.__hitbox_rect.top += 6
                    # bottom
                    if self.__hitbox_rect.bottom >= sprite.rect.top and int(self.__old_rect.bottom) <= int(sprite.old_rect.top):
                        self.__hitbox_rect.bottom = sprite.rect.top
                    self.__direction.y = 0

    def semi_collision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.__semi_collision_sprites:
                if sprite.rect.colliderect(self.__hitbox_rect):
                    if self.__hitbox_rect.bottom >= sprite.rect.top and int(self.__old_rect.bottom) <= sprite.old_rect.top:
                        self.__hitbox_rect.bottom = sprite.rect.top
                        if self.__direction.y > 0:
                            self.__direction.y = 0
    
    def uptade_timers(self):
        for timer in self.timers.values():
            timer.update()

    def animate(self, dt):
        self.__frame_index += get_animation_speed() * dt
        if self.__state == 'attack' and self.__frame_index >= len( self.__frames[self.__state] ):
            self.__state = 'idle'
        self.__image = self.__frames[self.__state][int( self.__frame_index % len( self.__frames[self.__state] ) )]
        self.__image = self.__image if self.__facing_right else pygame.transform.flip( self.__image, True, False )

        if self.__attacking and self.__frame_index > len( self.__frames[self.__state] ):
            self.__attacking = False

    def getstate(self):
        if self.__on_surface['floor']:
            if self.__attacking:
                self.__state = 'attack'
            else:
                self.__state = 'idle' if self.__direction.x == 0 else 'run'
        else:
            if self.__attacking:
                self.__state = 'air_attack'
            else:
                if any( ( self.__on_surface['left'], self.__on_surface['right'] ) ):
                    self.__state = 'wall'
                else:
                    self.__state = 'jump' if self.__direction.y < 0 else 'fall'

    def update(self, dt):
        self.__old_rect = self.__hitbox_rect.copy()
        self.uptade_timers()
        
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()

        self.getstate()
        self.animate(dt)
        ##print(self.__on_surface)
