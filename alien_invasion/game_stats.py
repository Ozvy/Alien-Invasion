import pygame
import pathlib
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
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
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')




    def reset_stats(self):
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level= 1

    def update(self, collisions):

        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_score(self, collisions):
        for alien in collisions:
            self.score += self.settings.alien_points
    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
            # print(self.max_score)
    def _update_hi_score(self):
        if self.score > self.hi_score:
            self.hi_score = self.score
            # print(self.hi_score)

    def update_level(self):
        self.level += 1



        