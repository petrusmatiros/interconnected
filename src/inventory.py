from key import *
class Inventory():
    """
    Class to represent the inventory of a character.
    """
    def __init__(self):
        """Initializes a new Inventory object
        """
        self.keys = []
        self.max_red = 3
        self.max_purple = 1
        
    def add_key(self, keycolor):
        """Adds a key to the inventory
        """
        if keycolor == Color.RED:
            if self.get_amount(keycolor) < self.max_red:
                self.keys.append(keycolor)
        elif keycolor == Color.PURPLE:
            if self.get_amount(keycolor) < self.max_purple:
                self.keys.append(keycolor)
                
    def get_amount(self, keycolor):
        """Returns the amount of the specified key
        """
        key_count = 0
        
        if len(self.keys) == 0:
            return 0
        
        for key in self.keys:
            if key == keycolor:
                key_count += 1
        
        return key_count

        
        
        
