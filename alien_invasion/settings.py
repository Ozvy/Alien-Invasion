from pathlib import Path

class Settings:
    '''
    Allows the user to change certain things about the game if they wanted to.
    '''
    def __init__(self):
        '''
        Some aspects of the game that can be changed easily. Includes the screen and ship's size and image used.
        '''
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2.png'
        self.ship_w = 120
        self.ship_h = 40
        self.ship_speed = 5
        self.starting_ship_count = 1

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast2.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        self.bullet_speed = 7
        self.bullet_w = 80
        self.bullet_h = 25
        self.bullet_amount = 5

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_speed = 4
        self.fleet_direction = 1
        self.fleet_drop_speed = 5
    