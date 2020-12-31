import math
import random

from asteroid import Asteroid
from torpedo import Torpedo
from screen import Screen
from ship import Ship
import sys



DEFAULT_ASTEROIDS_NUM = 5
ASTEROID_SPEED = [-4, -3, -2, -1, 1, 2, 3, 4]


class GameRunner:
    def __init__(self, asteroids_amount):
        self.__num = 0
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.max_coordinate = (self.__screen_max_x, self.__screen_max_y)
        self.min_coordinate = (self.__screen_min_x, self.__screen_min_y)

        x, y = self.random_spot()
        self.__ship = Ship(x, y, 3)
        self.asteroid_dict = {}
        self.create_asteroid()
        self.torpedo_dict = {}
        self.__score = 0
        self.torpedo_loops = {}

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
        if self.__screen.should_end():
            self.__screen.show_message("Goodbye coward! ", "Run player, run and never come back.")
            self.__screen.end_game()
            sys.exit()
        self.__screen.draw_ship(self.__ship.get_x(), self.__ship.get_y(), self.__ship.get_heading())
        if self.__screen.is_space_pressed():
            if len(self.torpedo_dict) < 10:
                self.create_torpedo()
        torpedo_key_to_delete = self.torpedo_timeout()
        if torpedo_key_to_delete is not None:
            self.__screen.unregister_torpedo(self.torpedo_dict[torpedo_key_to_delete])
            del self.torpedo_dict[torpedo_key_to_delete]
        self.move_torpedo()
        for key, value in self.asteroid_dict.items():
            self.__screen.draw_asteroid(value, value.get_x(), value.get_y())
        self.move_asteroids()
        self.move_ship()
        astroid_key_to_delete = self.ship_collision()
        if astroid_key_to_delete:
            del self.asteroid_dict[astroid_key_to_delete]
        keys = self.asteroid_collision()
        if keys:
            del self.asteroid_dict[keys[0]]
            del self.torpedo_dict[keys[1]]
        if len(self.asteroid_dict) == 0:
            self.__screen.show_message("You are the winner my friend! ", "Actually we are the winners, because we gonna"
                                                                         " get a 100 while you are playing games.")
            self.__screen.end_game()
            sys.exit()

    def torpedo_timeout(self):
        for key, value in self.torpedo_dict.items():
            self.__screen.draw_torpedo(value, value.get_x(), value.get_y(), value.get_heading())
            self.torpedo_loops[key] += 1
            if self.torpedo_loops[key] > 200:
                return key

    def random_spot(self):
        x = random.randint(self.min_coordinate[0], self.max_coordinate[0])
        y = random.randint(self.min_coordinate[1], self.max_coordinate[1])
        return x, y

    def create_asteroid(self, amount=DEFAULT_ASTEROIDS_NUM):
        for num in range(amount):
            x, y = self.random_spot()
            asteroid = Asteroid(x, y, 3)
            asteroid.set_x_speed(random.choice(ASTEROID_SPEED))
            asteroid.set_y_speed(random.choice(ASTEROID_SPEED))
            while asteroid.has_intersection(self.__ship):
                asteroid.set_x(random.randint(self.min_coordinate[0], self.max_coordinate[0]))
                asteroid.set_y(random.randint(self.min_coordinate[1], self.max_coordinate[1]))
            self.__screen.register_asteroid(asteroid, 3)
            self.asteroid_dict[id(asteroid)] = asteroid

    def create_torpedo(self):
        x = self.__ship.get_x()
        y = self.__ship.get_y()
        torpedo = Torpedo(x, y)
        torpedo.set_x_speed(self.__ship.get_x_speed() + (2 * math.cos(math.radians(self.__ship.get_heading()))))
        torpedo.set_y_speed(self.__ship.get_y_speed() + (2 * math.sin(math.radians(self.__ship.get_heading()))))
        torpedo.set_heading = self.__ship.get_heading()
        self.__screen.register_torpedo(torpedo)
        self.torpedo_dict[id(torpedo)] = torpedo
        self.torpedo_loops[id(torpedo)] = 0

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
            self.move_function(value)

    def move_torpedo(self):
        for key, value in self.torpedo_dict.items():
            self.move_function(value)

    def ship_collision(self):
        for key, value in self.asteroid_dict.items():
            if value.has_intersection(self.__ship):
                self.__ship.set_lives(self.__ship.get_lives() - 1)
                if self.__ship.get_lives() is not 0:
                    self.__screen.remove_life()
                else:
                    self.__screen.show_message("You lost the game! ", "Practice makes perfect.")
                    self.__screen.end_game()
                    sys.exit()
                self.__screen.show_message("Be careful! ", "Asteroid id " + str(key) + " collided with your ship.")
                self.__screen.unregister_asteroid(value)
                return key

    def asteroid_collision(self):
        for key, value in self.asteroid_dict.items():
            for torpedo_key, torpedo_value in self.torpedo_dict.items():
                if value.has_intersection(torpedo_value):
                    self.__screen.unregister_torpedo(torpedo_value)
                    self.split_asteroids(value, torpedo_value)
                    self.count_points(value)
                    return key, torpedo_key

    def count_points(self, asteroid):
        if asteroid.get_size() == 3:
            self.__screen.set_score(self.__score + 20)
            self.__score = self.__score + 20
        elif asteroid.get_size() == 2:
            self.__screen.set_score(self.__score + 50)
            self.__score = self.__score + 50
        elif asteroid.get_size() == 1:
            self.__screen.set_score(self.__score + 100)
            self.__score = self.__score + 100

    def split_asteroids(self, asteroid, torpedo):
        if asteroid.get_size() != 1:
            size = asteroid.get_size() - 1
            self.__screen.unregister_asteroid(asteroid)
            x, y = asteroid.get_x(), asteroid.get_y()
            x_speed, y_speed = self.get_new_speed(asteroid, torpedo)
            asteroid1 = Asteroid(x, y, size)
            asteroid1.set_x_speed(x_speed)
            asteroid1.set_x_speed(y_speed)
            asteroid2 = Asteroid(x, y, size)
            asteroid2.set_x_speed(-x_speed)
            asteroid2.set_x_speed(-y_speed)
            asteroid1.set_x(x)
            asteroid1.set_y(y)
            asteroid2.set_x(x)
            asteroid2.set_y(y)
            self.__screen.register_asteroid(asteroid1, size)
            self.__screen.register_asteroid(asteroid2, size)
            self.__screen.draw_asteroid(asteroid1, x, y)
            self.__screen.draw_asteroid(asteroid2, x, y)
            self.asteroid_dict[id(asteroid1)] = asteroid1
            self.asteroid_dict[id(asteroid2)] = asteroid2
        else:
            self.__screen.unregister_asteroid(asteroid)

    def get_new_speed(self, asteroid, torpedo):
        x_speed_asteroid = asteroid.get_x_speed()
        y_speed_asteroid = asteroid.get_y_speed()
        x_speed_torpedo = torpedo.get_x_speed()
        y_speed_torpedo = torpedo.get_y_speed()
        new_x_speed = (x_speed_torpedo + x_speed_asteroid) / \
                      (x_speed_asteroid ** 2 + y_speed_asteroid ** 2) ** 0.5
        new_y_speed = (y_speed_torpedo + y_speed_asteroid) / \
                      (x_speed_asteroid ** 2 + y_speed_asteroid ** 2) ** 0.5
        return new_x_speed, new_y_speed


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
