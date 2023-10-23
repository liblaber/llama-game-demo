from typing import List
from models.common import Direction

direction_to_coordinate = {"right": 1, "left": -1, "up": -1, "down": 1}


def convert_step_to_coordination(direction: Direction, steps: int) -> List[int]:
    if direction is Direction.RIGHT or direction is Direction.LEFT:
        return [0, steps * direction_to_coordinate[direction]]
    if direction is Direction.UP or direction is Direction.DOWN:
        return [steps * direction_to_coordinate[direction], 0]
    return [0,0]