import pygame
from typing import TYPE_CHECKING
from settings import Settings
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """
    Represents the fleet of aliens in the game.  The AlienFleet class is responsible for:
    -  Creating and managing a group of Alien instances.
    -  Calculating the size and offsets for positioning the alien fleet.
    -  Creating the rectangular formation of aliens.
    -  Updating the fleet's movement and checking for edge collisions.
    -  Drawing the entire fleet on the screen.
    -  Checking for collisions between the fleet and other game elements.
    -  Checking if the fleet has reached the right edge of the screen.
    -  Checking if the fleet has been destroyed.


    Methods:
        __init__(self, game): Initializes the fleet.
        create_fleet(self): Creates the alien fleet.
        _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset): Creates a rectangular formation of aliens.
        calculate_offsets(self, alien_h, fleet_h): Calculates the x and y offsets to center the fleet.
        calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h): Calculates the width and height of the fleet.
        _create_alien(self, current_x, current_y): Creates a single alien and adds it to the fleet.
        _check_fleet_edges(self): Checks if any alien has reached the top or bottom edge of the screen.
        _drop_alien_fleet(self): Moves the entire fleet right when colliding with the top or bottom edges of the screen.
        update_fleet(self): Updates the fleet's position and checks for edge collisions.
        draw(self): Renders the fleet.
        check_collisions(self, other_group): Checks for collisions between the aliens and the ship/bullets.
        check_fleet_right(self): Checks if the fleet has reached the right edge of the screen, if it does, reset the level and have the player lose a life.
        check_destroyed_status(self): Checks if the fleet has been destroyed.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initializes the fleet.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()

    def create_fleet(self):
        """
        Creates the fleet.
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_h, fleet_h)

        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Creates a rectangular formation of aliens.

        Args:
            alien_w (int): The width of a single alien.
            alien_h (int): The height of a single alien.
            fleet_w (int): The number of aliens in a row.
            fleet_h (int): The number of rows in the fleet.
            x_offset (int): The horizontal offset for the fleet's starting position.
            y_offset (int): The vertical offset for the fleet's starting position.
        """
        for col in range(fleet_h):
            for row in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_h, fleet_h):
        """
        Calculates the x and y offsets to center the fleet.

        """
        half_screen = self.settings.screen_h // 2
        fleet_vertical_space = fleet_h * alien_h
        x_offset = 0
        y_offset = int((half_screen - fleet_vertical_space) // 2)
        return x_offset, y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """
        Calculates the width and height of the fleet.
        """
        fleet_w = ((screen_w / 1.5) // alien_w)
        fleet_h = ((screen_h / 2) // alien_h)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int):
        """
        Creates a single alien and adds it to the fleet.

        Args:
            current_x (int): The horizontal position of the alien.
            current_y (int): The vertical position of the alien.
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """
        Checks if any alien has reached the edge of the screen, and restarts the level if so.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.settings.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        """
        Moves the entire fleet right when colliding with the top or bottom edges of the screen.
        """
        for alien in self.fleet:
            alien.x += self.settings.fleet_drop_speed

    def update_fleet(self):
        """
        Updates the fleet's position and checks for edge collisions.
        """
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """
        Renders the fleet.
        """
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """
        Checks for collisions between the aliens and the ship/bullets.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_right(self):
        """
        Checks if the fleet has reached the right edge of the screen, if it does, reset the level and have the player lose a life.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.right >= self.settings.screen_w:
                return True
        return False

    def check_destroyed_status(self):
        """
        Checks if the fleet has been destroyed.
        """
        return not self.fleet