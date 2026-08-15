import pygame 

class Ship:
    
    def __init__(self , ai_game) -> None:
        """Initialize the ship and setting its inittial position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        

        """Load the ship image and get its rect."""
        self.image = pygame.image.load('E:\PROGRAMMING\PYTHON\Aliens_invasion\Images\Ship1.bmp')
        self.rect = self.image.get_rect()

        """Store the decimal value for horizontal distance of ship"""
        self.x = float(self.rect.x)


        """Start each new ship at the bottom centre of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom

        """Movement flag"""
        self.moving_right = False
        self.moving_left = False

       
    def update(self): #For countinous moving
        """Update the position of ship based on key press or movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
           # self.rect.x += 1
           """Updating ship speed"""
           self.x += self.settings.ship_speed
        
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed
        
        """Update rect object"""
        self.rect.x = self.x

    def blitme(self):
        """Draw ship at current location"""
        self.screen.blit(self.image , self.rect)

    def center_ship(self):
        """Center the ship to the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)