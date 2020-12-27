class Asteroid:
    """
    Add class description here
    """

    def __init__(self, x, x_speed, y, y_speed, size):
        """
        A constructor for a Asteroid object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.x = x
        self.x_speed = x_speed
        self.y = y
        self.y_speed = y_speed
        self.size = size