import pygame

class HUD:
    """
    Manages the hud. This class is responsible for:

        - The current and high score
        - The max score achieved in the current session
        - The current level in the game
        - The number of remaining lives

    Attributes:
        padding (int): The spacing in pixels between HUD elements and screen edges.

    Methods:
        __init__(self, game): Initializes the HUD.
        setup_life_image(self): Renders the life image.
        update_scores(self): Updates the the current score, max score, and high score on the counter.
        _draw_lives(self): Renders the remaining lives on the screen.
        draw(self): Renders the score and level text on the screen.
    """
    def __init__(self, game):
        """
        Initializes the HUD.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file, self.settings.HUD_font_size)
        self.padding = 20
        self.update_scores()
        self.setup_life_image()
        self.update_level()

    def setup_life_image(self):
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image, (
            self.settings.ship_w, self.settings.ship_h
            ))
        self.life_rect = self.life_image.get_rect()

    
    def update_scores(self):
        self._update_max_score()
        self._update_score()
        self._update_hi_score()
    
    def _update_score(self):
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True, self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def _update_max_score(self):
        max_score_str = f'Max Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True, self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self):
        hi_score_str = f'Hi Score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True, self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.right = self.boundaries.right - self.padding
        self.hi_score_rect.midtop = (self.boundaries.centerx,self.padding)
    def update_level(self):
        level_str = f'Level: {self.game_stats.level: ,.0f}'
        self.level_image = self.font.render(level_str, True, self.settings.text_color, None)
        self.level_rect = self.score_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.life_rect.bottom + self.padding

    def _draw_lives(self):
        """
        Renders the remaining lives on the screen.
        """
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self):
        """
        Renders the score and level text on the screen.
        """
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()
