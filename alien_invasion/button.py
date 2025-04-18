import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal  # Not used in this class, but kept for consistency

class Button:
    """
    Represents a button in the game.  The Button class is responsible for:
    -   Creating a rectangular button with text.
    -   Centering the button on the screen.
    -   Rendering the button's text.
    -   Drawing the button and its text on the screen.
    -   Checking if the button has been clicked.

    Attributes:
        font (pygame.font.Font): The font used for the button's text.
        rect (pygame.Rect): The rectangle that defines the button's size and position.
        msg_image (pygame.Surface): The rendered image of the button's text.
        msg_image_rect (pygame.Rect): The rectangle for the text image's position.

    Methods:
        __init__(self, game, msg): Initializes the button.
        _prep_msg(self, msg): Prepares the button's text image.
        draw(self): Renders the button and the text.
        check_clicked(self, mouse_pos): Checks if the button has been clicked. Returns true if so.
    """
    def __init__(self, game: 'AlienInvasion', msg):
        """
        Initializes the button.

        Args:
            msg (str): The text to display on the button.
        """
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.boundaries = game.screen.get_rect()

        self.font = pygame.font.Font(self.settings.font_file, self.settings.button_font_size)
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Prepares the button's text.
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """
        Renders the button and the text.
        """
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """
        Checks if the button has been clicked. Returns true if so.
        """
        return self.rect.collidepoint(mouse_pos)