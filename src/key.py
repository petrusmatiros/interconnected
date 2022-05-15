from enum import Enum
class Color(Enum):
    RED = "Red"
    PURPLE = "Purple"

class Key():
    """
    Class to represent the keys in the game
    """
    def __init__(self, color, description):
        """Initializes a new Key object
		"""
        self.color = color
        self.description = description

    def get_color(self):
        """Returns the color of the key
		"""
        return self.color
    
    def get_description(self):
        """Returns the description of the key
		"""
        return self.description
