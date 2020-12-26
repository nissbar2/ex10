
class Ship:
    """
    Add class description here
    """

    def __init__(self, x, x_speed, y, y_speed, direction):
        """
        A constructor for a Car object
        :param x: A float representing the ship x coordinate
        :param x_speed: A positive int representing the car's length.
        :param y: A tuple representing the car's head (row, col) location
        :param y_speed: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.x = x
        self.x_speed = x_speed
        self.y = y
        self.y_speed = y_speed
        self.direction = direction