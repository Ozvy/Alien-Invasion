import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import ship
from arsenal import Arsenal
# from alien import Alien
from alien_fleet import AlienFleet
from time import sleep
from button import Button

class AlienInvasion:
    """
    The class that runs basically everything about this game.

    Attributes:
        event: the event that is fired.
    Methods: 
        run_game(self): Allows the game to run and function, and sets framerate .
        _check_events(self): Makes sure the game properly closes when the user closes the game, and checks for
        other events that run in the game.
        _update_screen(self): displays everything on the screen and updates anything on the screen to its new position.
        _check_keydown_event(self, event): Checks if the key is pressed down. Keys:
            K_Right: fires an event that makes the ship move right.
            K_Left: Ditto, but left.
            K_Space: Plays a sound when pressed and makes the ship fire a bullet.
            K_q: exits out of the game.
        _check_keyup_event(self, event): Checks if the key is not being pressed. if it isn't pressed, keep the ship completely still.
    """
    def __init__(self):
        """
        Sets the display resolution and name of the window, as well as ensures the program runs. 
        Runs at the number of fps that is displayed in settings.py. 
        """
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)

        self.ship = ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.play_button = Button(self, 'Play')
        self.game_active = False

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)
       

        
        


    def run_game(self):
        """
        Allows the game to run and function, and sets framerate . Also displays the game BG.
        """
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        '''
        Checks the ship, aliens and the bottom of the screen, as well as the collisions of projectiles.
        '''
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()

        if self.alien_fleet.check_fleet_right():
            self._check_game_status()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
        
    def _check_game_status(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
        print(self.game_stats.ships_left)
        
        
    
    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
    
    def restart_game (self):
        self.settings.initialize_dynamic_settings()
        
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)
        # reset game stats
        # update hud scores

    def _update_screen(self):
        '''
         displays everything on the screen and updates anything on the screen to its new position.
        '''
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        self.alien_fleet.draw()
        pygame.display.flip()


    def _check_events(self):
        '''
        Checks for button pressed events and the game quitting.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

            

    def _check_keydown_event(self, event):
        '''
        Checks if the key is pressed down. if it is, move the ship. 
        
        Keys:
            K_Up: fires an event that makes the ship move up.
            K_Down: Ditto, but down.
            K_Space: Plays a sound when pressed and makes the ship fire a bullet.
            K_q: exits out of the game.
        '''
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(300)
                
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

    def _check_keyup_event(self, event):
        '''
        Checks if the key is not being pressed. if it isn't pressed, keep the ship completely still.
        '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


                    


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
