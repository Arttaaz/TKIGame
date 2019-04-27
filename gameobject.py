class GameObject:

    def __init__(self, image, id = 0,  collide=False):
        self.image = image
        self.collide = collide
        self.rect = image.get_rect()
        self.id = id
    def update(self):
        pass
        
    def draw(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)

    def __str__(self):
        return str(self.id)

    
