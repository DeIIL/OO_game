from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft =  position)
    
    # movement
        self.direction = vector() #vector which came from alas in settings.py ps:no parameters passed means de directions are 0
        self.speed = 200


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0) #vector for if for example both right and left keys are pressed in the same frame they subtraction each other 
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_d]:
            input_vector.x += 1
        self.direction = input_vector.normalize() if input_vector else input_vector #lenght of the vector always be 1

    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)