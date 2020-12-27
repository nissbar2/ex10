import math
import random

from asteroid import Asteroid
from torpedo import Torpedo

import screen
from screen import Screen
import sys

from ship import Ship

DEFAULT_ASTEROIDS_NUM = 5
ASTEROID_SPEED = [-4, -3, -2, -1, 1, 2, 3, 4]
"""
אמורה לייצר את האובייקטים השונים של המשחק
להכיל מימוש שלה אינטרקציות השונות ביניהן ולדאוג לרצף פעילות התקין של המשחק
ניתן להוסיף פונקציות
"""


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.max_coordinate = (self.__screen_max_x, self.__screen_max_y)
        self.min_coordinate = (self.__screen_min_x, self.__screen_min_y)

        self.__ship = self.create_ship()
        self.asteroid_dict = {}
        self.create_asteroid()

        self.__torpedo = self.create_torpedo()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # TODO: Your code goes here
        self.__screen.draw_ship(self.__ship.get_x(), self.__ship.get_y(), self.__ship.get_heading())
        if self.__screen.is_space_pressed():
            self.create_torpedo()
            self.__screen.draw_torpedo(self.__torpedo, self.__torpedo.get_x(), self.__torpedo.get_y(),
                                       self.__torpedo.get_heading())
        self.move_asteroids()
        self.move_ship()

    def create_ship(self):
        x = random.randint(self.min_coordinate[0], self.max_coordinate[0])
        y = random.randint(self.min_coordinate[1], self.max_coordinate[1])
        x_speed = 0
        y_speed = 0
        heading = 0
        return Ship(x, x_speed, y, y_speed, heading)

    def create_asteroid(self):
        for num in range(DEFAULT_ASTEROIDS_NUM):
            x = random.randint(self.min_coordinate[0], self.max_coordinate[0])
            y = random.randint(self.min_coordinate[1], self.max_coordinate[1])
            x_speed = random.choice(ASTEROID_SPEED)
            y_speed = random.choice(ASTEROID_SPEED)
            asteroid = Asteroid(x, x_speed, y, y_speed, 3)
            self.__screen.register_asteroid(asteroid, 3)
            self.__screen.draw_asteroid(asteroid, x, y)
            self.asteroid_dict[id(asteroid)] = asteroid

    def create_torpedo(self):
            x = self.__ship.get_x()
            y = self.__ship.get_y()
            x_speed = random.choice(ASTEROID_SPEED)
            y_speed = random.choice(ASTEROID_SPEED)
            heading = self.__ship.get_heading()
            return Torpedo(x, x_speed, y, y_speed, heading)
        # torpedo = Torpedo(x, x_speed, y, y_speed, heading)
        # self.torpedo[Torpedo(x, x_speed, y, y_speed, heading)] = torpedo

    def move_function(self, obj):
        obj.set_x(self.__screen_min_x + (
                obj.get_x() + obj.get_x_speed() - self.__screen_min_x) %
                          (self.__screen_max_x - self.__screen_min_x))
        obj.set_y(self.__screen_min_y + (
                obj.get_y() + obj.get_y_speed() - self.__screen_min_y) %
                          (self.__screen_max_y - self.__screen_min_y))

    def move_ship(self):
        self.move_function(self.__ship)
        if self.__screen.is_left_pressed():
            heading = self.__ship.get_heading()
            self.__ship.set_heading(heading + 7)

        if self.__screen.is_right_pressed():
            heading = self.__ship.get_heading()
            self.__ship.set_heading(heading - 7)

        if self.__screen.is_up_pressed():
            self.__ship.set_x_speed(self.__ship.get_x_speed() + math.cos(math.radians(self.__ship.get_heading())))
            self.__ship.set_y_speed(self.__ship.get_y_speed() + math.sin(math.radians(self.__ship.get_heading())))

    def move_asteroids(self):
        for key, value in self.asteroid_dict.items():
            self.move_function(self.asteroid_dict[key])



def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
