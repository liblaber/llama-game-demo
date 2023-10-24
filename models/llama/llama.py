from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class LlamaColor(str, Enum):
    """
    The color of a llama.
    """
    black = "black"
    white = "white"
    red = "red"
    blue = "blue"
    green = "green"
    yellow = "yellow"
    orange = "orange"
    purple = "purple"
    cyan = "cyan"
    magenta = "magenta"
    lime = "lime"
    pink = "pink"
    teal = "teal"
    brown = "brown"
    navy = "navy"
    maroon = "maroon"
    olive = "olive"
    silver = "silver"
    gold = "gold"
    beige = "beige"
    turquoise = "turquoise"
    indigo = "indigo"
    coral = "coral"
    salmon = "salmon"
    chocolate = "chocolate"


    

class LlamaStatus(str, Enum):
    """
    Current status of the Llama
    """
    DEAD = "dead"
    ALIVE = "alive"

class LlamaInput(BaseModel):
    """
    A llama to create, with details of its name and color.
    """
    name: str = Field(description="The llamas name.")
    color: LlamaColor = Field(default= LlamaColor.white.value, description="The llamas name.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Libby",
                    "color": "black",
                }
            ]
        },
        "description": "A llama to create, with details of its name and color.",
        "from_attributes": True,
    }

    def update_color(self, color : LlamaColor ):
        self.color = color

class Llama(LlamaInput):
    """
    A llama, with details of it's name, color, status, current score, current coordinates and its steps list.
    """
    id: int = Field(description="The llamas name.")
    score: int = Field(default=0, description="Current score of the llama.")
    start_coordinates : List[int] = Field(default=[0,0], max_length=2, min_length=2, description="Start position of the llama.")
    curr_coordinates : List[int] = Field(default=[0,0], max_length=2, min_length=2, description="Current position of the llama.")
    steps_list : List[List[int]] = Field(default=[], description="The list of steps the llama has taken since the last time the move endpoint was called.")
    status: LlamaStatus = LlamaStatus.ALIVE.value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Libby",
                    "color": "black",
                    "id": 123,
                    "score": 12,
                    "start_coordinates": [0,0],
                    "curr_coordinates": [0,5],
                    "steps_list": [[0,0], [0,5]],
                    "status": "alive",
                }
            ],
             "description": "A llama to create, with details of its name and color.",
        },
        "from_attributes": True,
    }

    def set_color(self, color : LlamaColor) -> None:
        self.color = color

    def set_name(self, name : str) -> None:
        self.name = name

    def add_score(self, points : int) -> None:
        self.score += points
