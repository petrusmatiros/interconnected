

class Current():
    def __init__(self):
        # Boolean values for visited rooms and secret ending information
        self.SSD_visited = False
        self.internet_visited = False
        self.has_information = False
        self.inserted_information = False
        
        self.L1_visited = False
        self.L2_visited = False
        self.L3_visited = False
        
        # Boolean values for picking up keys
        self.red_key = False
        self.purple_key = False
        
        