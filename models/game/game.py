from typing import List
from pydantic import BaseModel, Field
from ..llama import LlamaStatus
from ..common import Direction

class MoveResult(BaseModel):
    """
    A llama to create, with details of its name and color.
    """
    id: int = Field(description="The llamas id.")
    score: int = Field(default= 0, description="Current score.")
    status: LlamaStatus = Field(default= LlamaStatus.ALIVE, description="Current Llama's status.")
    position: List[int]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 123,
                    "score": 5,
                    "status": "alive",
                    "position": [0, 4],
                }
            ]
        },
        "description": "The results of the llama's moves.",
        "from_attributes": True,
    }

class StepResult(BaseModel):
    """
    A llama to create, with details of its name and color.
    """
    id: int = Field(description="The llamas id.")
    direction: Direction = Field(default= Direction.RIGHT, description="The direction the llama will move in.")
    steps: int = Field(default = 0, description="The amount of steps the llama will take.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 123,
                    "direction": "right",
                    "steps": 5
                }
            ]
        },
        "description": "The steps the llama is going to take.",
        "from_attributes": True,
    }