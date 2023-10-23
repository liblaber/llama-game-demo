from enum import Enum
from typing import List
from pydantic import BaseModel
from models.llama import LlamaStatus

MAP_SIZE_X = 48
MAP_SIZE_Y = 10

class MapGridItem(Enum):
    EMPTY = 0
    OBJECT = -1
    COIN = 1

class StepResult(BaseModel):
    status: LlamaStatus
    score: int
    position: List[int]



MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

class Map(BaseModel):
    matrix: List[List[MapGridItem]]

    def update_map(self, step: List[int], start_point: List[int]) -> StepResult:
        score = 0
        step_y, step_x = step[0], step[1]
        start_y, start_x = start_point[0], start_point[1]
        if step_x != 0:
            iter = int(step_x / abs(step_x))
            i = iter
            while abs(i) <= abs(step_x):
                curr_x = start_x + i
                if self.matrix[start_y][curr_x] == MapGridItem.COIN:
                    score +=1
                    self.matrix[start_y][curr_x] = 0
                elif curr_x < 0 or curr_x > MAP_SIZE_X -1 or self.matrix[start_y][curr_x] == MapGridItem.OBJECT :
                    return { "status" : LlamaStatus.DEAD, "score": score, "position": [start_y, curr_x]}
                i += iter
            return { "status" : LlamaStatus.ALIVE, "score": score, "position": [start_y, curr_x ]}
        if step_y != 0:
            iter = int(step_y / abs(step_y))
            i = iter
            while abs(i) <= abs(step_y):
                curr_y = start_y + i
                if self.matrix[curr_y][start_x] == MapGridItem.COIN:
                    score +=1
                    self.matrix[curr_y][start_x] = 0
                elif curr_y < 0 or curr_y > MAP_SIZE_Y -1 or self.matrix[curr_y][start_x] == MapGridItem.OBJECT :
                    return { "status" : LlamaStatus.DEAD, "score": score, "position": [curr_y, start_x]}
                i += iter
            return { "status" : LlamaStatus.ALIVE, "score": score, "position": [curr_y, start_x]}
        return { "status" : LlamaStatus.ALIVE, "score": score, "position": start_point}
