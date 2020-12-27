import math
import random

import screen
from screen import Screen
import sys

from ship import Ship

DEFAULT_ASTEROIDS_NUM = 5

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
        self.__astroids = {}

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
        self.move_ship()

    def create_ship(self):
        x = random.triangular(self.min_coordinate[0], self.max_coordinate[0])
        y = random.triangular(self.min_coordinate[1], self.max_coordinate[1])
        x_speed = 0
        y_speed = 0
        heading = 0
        return Ship(x, x_speed, y, y_speed, heading)

    def move_ship(self):
        if self.__screen.is_left_pressed():
            heading = self.__ship.get_heading()
            self.__ship.set_heading(heading + 7)

        if self.__screen.is_right_pressed():
            heading = self.__ship.get_heading()
            self.__ship.set_heading(heading - 7)

        if self.__screen.is_up_pressed():
            self.__ship.set_x_speed(self.__ship.get_x_speed() + math.cos(self.__ship.get_heading()))

            self.__ship.set_y(self.__screen_min_x + (
                    self.__ship.get_x() + self.__ship.get_x_speed() - self.__screen_min_x) %
                              (self.__screen_max_x - self.__screen_min_x))

            self.__ship.set_y_speed(self.__ship.get_y_speed() + math.cos(self.__ship.get_heading()))

            self.__ship.set_x(self.__screen_min_y + (
                    self.__ship.get_y() + self.__ship.get_y_speed() - self.__screen_min_y) %
                              (self.__screen_max_y - self.__screen_min_y))






            print(self.__ship.get_x(), self.__ship.get_y(), self.__ship.get_x_speed(), self.__ship.get_y_speed(),
                  self.__ship.get_heading())


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
