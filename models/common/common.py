from enum import Enum

class Direction(str, Enum):
    """
    The possible directions a llama can take.
    """
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    
    def list():
        return list(map(lambda x: x.value, Direction._member_map_.values()))