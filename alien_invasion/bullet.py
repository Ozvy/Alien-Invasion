import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """
    Represents a bullet fired by the player's ship.

    Inherits from pygame.sprite.Sprite, allowing it to be easily managed in sprite groups.

    Attributes:
        
        x (float): The bullet's horizontal position.
    """
    def __init__(self, game: 'AlienInvasion'):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w, self.settings.bullet_h))

        self.rect = self.image.get_rect()
        self.rect.midleft = game.ship.rect.midleft
        self.x = float(self.rect.x)
        
    def update(self):
        self.x -= self.settings.bullet_speed
        self.rect.x = self.x
    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)