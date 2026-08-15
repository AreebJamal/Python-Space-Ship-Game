class Settings:
    #A class to store all setting of alien invasion
    def __init__(self) -> None:
        # Create setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (4, 6 ,38)
        #self.ship_speed = 1
        self.ship_limit = 3
        
        # Bullet settings
        #self.bullet_speed = 1
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (16 , 250 , 119)
        self.bullets_allowed = 5
         
        #Alien settings
        #self.alien_speed = 2
        self.fleet_dropspeed = 10
        """Fleet direction of 1 represent right , -1 represent left"""
        #self.fleet_direction = 1

        """How quickly the game speed up"""
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0

        """Fleet direc of 1 represent right and -1 represent left"""
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


