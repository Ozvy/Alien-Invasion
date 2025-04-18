import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """
    Tracks and manages game statistics for the Alien Invasion game.

    This class is responsible for 
    - Storing and updating information such as the 
    current score, the high score, the number of ships remaining, and the current game level. 
    - Handling saving and loading the high score from a file to persist across game sessions.

    Attributes:
        max_score (int): The highest score achieved in the current game session.
        hi_score (int): The overall high score, loaded from and saved to a file.
        ships_left (int): The number of player ships remaining.
        score (int): The current score of the game.
        level (int): The current level of the game.
    Methods:
        __init__(self, game: 'AlienInvasion'): Initializes the game stats.
        init_saved_scores(self): Initializes the high score by grabbing the score from a saved JSON file.
        save_scores(self): Writes the new high score to the JSON file. Handles errors with the file being missing.
        reset_stats(self): Resets the level, lives, and score when a new game starts.
        update(self, collisions): Updates game statistics based on game events.
        update_level(self): Increases the current game level.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initializes the game stats.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """
        Initializes the high score by grabbing the score from a saved JSON file.
        """
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
            if not contents:
                print('file empty')
            
        else:
            self.hi_score = 0
            self.save_scores()
    
    def save_scores(self):
        """
        Writes the new high score to the JSON file. Handles errors with the file being missing.
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')




    def reset_stats(self):
        """
        Resets the level, lives, and score when a new game starts.
        """
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level= 1

    def update(self, collisions):
        """
        Updates the scores when called.
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_score(self, collisions):
        """
        Updates the score when an alien is destroyed.
        """
        for alien in collisions:
            self.score += self.settings.alien_points
    def _update_max_score(self):
        """
        Updates max score if the score is bigger than the max score.
        """
        if self.score > self.max_score:
            self.max_score = self.score
            # print(self.max_score)
    def _update_hi_score(self):
        """
        Updates hi score if the score is bigger than the hi score.
        """
        if self.score > self.hi_score:
            self.hi_score = self.score
            # print(self.hi_score)

    def update_level(self):
        """
        Increases the current game level.
        """
        self.level += 1



        