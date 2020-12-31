class Asteroid:
    """
    Add class description here
    """

    def __init__(self, x, y, size):
        """
        A constructor for a Asteroid object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__x = x
        self.__x_speed = 0
        self.__y = y
        self.__y_speed = 0
        self.__size = size

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

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def radius(self):
        return self.__size * 10 - 5

    def has_intersection(self, obj):
        distance = ((obj.get_x() - self.__x) ** 2 + (obj.get_y() - self.__y) ** 2) ** 0.5
        if distance <= self.radius() + obj.radius():
            return True
        return False