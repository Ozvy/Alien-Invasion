import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """
    Represents an individual alien in the fleet.  The Alien class is responsible for:
    -  Storing and updating the alien's position on the screen.
    -  Checking if the alien has reached the edge of the screen.
    -  Rendering the alien appearance.
    
    
    Attributes:
        fleet (AlienFleet): The fleet to which this alien belongs.
        x (float): The alien's horizontal position as a float.
        y (float): The alien's vertical position as a float.

    Methods:
        update(self): Updates the alien's position.
        check_edges(self): Checks if the alien has reached the top or bottom of the screen and returns true if so.
        draw_alien(self): Renders the alien.
    
    """
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """
        Initializes the aliens appearnce and their coordinates.
        """
        super().__init__()
        self.fleet = fleet

        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w, self.settings.alien_h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
    def update(self):
        """
        Updates the alien's position.
        """
        self.y += self.settings.fleet_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y
        
    def check_edges(self):
        """
        check_edges(self): Checks if the alien has reached the top or bottom of the screen and returns true if so.
        """
        return (self.rect.bottom >= self.boundaries.bottom or self.rect.top <= self.boundaries.top)
    def draw_alien(self):
        """
        Renders the alien.
        """
        self.screen.blit(self.image, self.rect)
    
