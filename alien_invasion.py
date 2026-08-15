import sys
from time import sleep
import pygame
from settings import Settings
from bullets import Bullets
from game_stats import Gamestats
from button import Button
from alien import Alien
from ship import Ship


class ALieninvasion:

    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings()
        """Create a game window size and caption"""
        #self.screen = pygame.display.set_mode((1200 , 800))
        self.screen = pygame.display.set_mode((self.settings.screen_width , self.settings.screen_height))
        pygame.display.set_caption("ALIEN INVASION")

        """Create an instance to store gamestats"""
        self.stats = Gamestats(self)

        self.ship = Ship(self)
        """Create bullet group"""
        self.bullets = pygame.sprite.Group()
        """Creating aliens fleet"""
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        """Make the play button"""
        self.play_button = Button(self , "Play")

        """Setting background color"""
        #self.bg_color = (230 , 230 , 230)



    def run_game(self):
        """start the main loop"""
        while True:
            self._check_events() # helper method used to simply 

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
                
            self._update_screen() #  the code , Leading underscore define it
            

            """watch for keyboard and mouse event"""
            #for event in pygame.event.get():
              #  """Exit the window through sys when we click the X"""
                #if event.type == pygame.QUIT:
                   # sys.exit()                   


    def _check_events(self):
            """watch for keyboard and mouse event"""
            for event in pygame.event.get():
                """Exit the window through sys when we click the X"""
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                          
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
                     
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)


    def _check_play_button(self , mouse_pos):
        """Start the new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
           """Reset the game statistics"""
           self.settings.initialize_dynamic_settings()
           self.stats.reset_stats()
           self.stats.game_active = True

           """Get rid of any remaining aliens and bullets"""
           self.aliens.empty()
           self.bullets.empty()

           """Create new fleet and center the ship"""
           self._create_fleet()
           self.ship.center_ship()

           """Hide the mouse cursor"""
           pygame.mouse.set_visible(False)

    
    def _check_keydown_events(self , event):
         """Respond to keypresses"""
         if event.key == pygame.K_RIGHT: 
            """Move the ship to right continously"""
            self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
            """Move the ship to the left continously"""
            self.ship.moving_left = True

         elif event.key == pygame.K_q:
             sys.exit()

         elif event.key == pygame.K_SPACE:
             self._fire_bullets()



    def _check_keyup_events(self , event):
         """Respond to key releases"""
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
    
    def _fire_bullets(self):

        """Create the other bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullets =Bullets(self)
            self.bullets.add(new_bullets)


    def _update_bullets(self):
        """Update the position of new bullets and get rid of old bullet"""
        self.bullets.update()
        
        """Get rid of bullets that has disappeared"""
        for bullets in self.bullets.copy():
            if bullets.rect.bottom <= 0:
                self.bullets.remove(bullets)
        
        self._check_bullet_alien_collision()


    def _check_bullet_alien_collision(self):
            """Check for any bullet hit the alien and get rid of them bith bullet and alien"""
            collisions = pygame.sprite.groupcollide(self.bullets , self.aliens , True , True)
            
            if not self.aliens:
                """Destroy existing bullets and create new fleet"""
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()

            #print(len(self.bullets))
         

    def _update_alien(self):
        """Check if fleet is at an edge"""
        self._check_fleetedge()
        """Update the position of all aliens in a fleet"""
        self.aliens.update()
        """Looking for ship and alien collision"""
        if pygame.sprite.spritecollideany(self.ship , self.aliens):
            #print("SHIP HIT!!!")
            self._ship_hit()
        
        """Look for alien hit the bottom of the screen"""
        self._check_alien_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by alien"""
        if self.stats.ship_left > 0:
            #Decrement ship left
            self.stats.ship_left -= 1

            # Get rid of any alien and bullet
            self.aliens.empty()
            self.bullets.empty()

            #Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        """Check if any alien has reached the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of alien"""
        #Make an alien 
        #Spacing between each alien is equal to the width of alien
        alien = Alien(self)
        alien_width , alien_height= alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_alien = available_space_x // (2*alien_width)

        """Determine the no. of rows of aliens fit on the screen"""
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3*alien_height) - (3*ship_height)
        number_rows = available_space_y // (2*alien_height)
    
        """Create the full fleet of alien"""
        for row_no in range(number_rows):
             for alien_no in range(number_alien):
                 self._create_alien(alien_no , row_no)
           

    def _create_alien(self , alien_no , row_no):
            alien = Alien(self)
            alien_width , alien_height= alien.rect.size
            alien.x = alien_width + 2*alien_width*alien_no
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2*alien.rect.height*row_no
            self.aliens.add(alien)
     
    def _check_fleetedge(self):
        """Respond appropriately if any aliens reached either edge"""
        for aliens in self.aliens.sprites():
            if aliens.check_edges():
                self._change_fleetdir()
                break

    def _change_fleetdir(self):
        """Drop the entire fleet and change the fleet direction"""
        for aliens in self.aliens.sprites():
            aliens.rect.y += self.settings.fleet_dropspeed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
            """update the image and centre it to the new screen"""
            
            """Redraw the screen every time during each iteration"""
            #self.screen.fill(self.bg_color)
            self.screen.fill(self.settings.bg_color)

            self.ship.blitme()

            for bullets in self.bullets.sprites():
                bullets.draw_bullets()

            self.aliens.draw(self.screen)

            """Draw the play button if the game is inactive"""
            if not self.stats.game_active:
                self.play_button.draw_button()

            """It shows the recently drawn screen"""
            pygame.display.flip()



if __name__ == '__main__':
    """Making game instance and run the game"""
    ai = ALieninvasion()
    ai.run_game()


