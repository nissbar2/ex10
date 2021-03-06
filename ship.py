import screen
import random

class Ship:
    """
    Add class description here
    """
    def __init__(self, x, y, lives):
        """
        A constructor for a ship object
        :param x: A float representing the ship x coordinate
        :param x_speed: .
        :param y:
        :param y_speed:
        """
        self.__x = x
        self.__x_speed = 0
        self.__y = y
        self.__y_speed = 0
        self.__heading = 0
        self.__radius = 1
        self.__lives = lives

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y):
        self.__y = y

    def get_x_speed(self):
        return self.__x_speed

    def set_x_speed(self, x_speed):
        self.__x_speed = x_speed

    def get_y_speed(self):
        return self.__y_speed

    def set_y_speed(self, y_speed):
        self.__y_speed = y_speed

    def get_heading(self):
        return self.__heading

    def set_heading(self, heading):
        self.__heading = heading

    def radius(self):
        return self.__radius

    def get_lives(self):
        return self.__lives

    def set_lives(self, lives):
        self.__lives = lives
