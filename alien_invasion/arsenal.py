import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    """
    Manages the ship's arsenal of bullets.

    This class is responsible for:
    - Initializing a group to hold bullet objects.
    - Updating the position of all active bullets.
    - Removing bullets that have gone off-screen.
    - Drawing the active bullets on the screen.
    - Creating and adding new bullets to the arsenal when the ship fires,
    doesn't fire anymore when the max count has been reached until the bullets are removed.

    Attributes:
        arsenal (pygame.sprite.Group): A Pygame sprite group that holds all the active Bullet objects
            fired by the ship.
    """
    def __init__ (self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):

        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        for bullet in self.arsenal.copy():
            if bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_w:
                self.arsenal.remove(bullet)
    def draw(self):
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
