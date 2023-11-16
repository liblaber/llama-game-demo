"""
The routes for controlling a llama
"""

import json
from enum import Enum
from typing import List
from fastapi import APIRouter, HTTPException, Query, Body, Path, status
from dummy import LlamaDummy
from models.llama import LlamaInput, Llama
from models.common import Direction
from models.game import MoveResult, StepResult
from game_logic.maps import MAP, Map, LlamaStatus, MapGridItem
from game_logic.calculations import convert_step_to_coordination
from connection_manager import manager


# for testing
llamas_dummy = LlamaDummy()
llama1 = LlamaInput(name="libby")
llamas_dummy.add_llama(llama1)
llama2 = LlamaInput(name="libby2", color="black")
llamas_dummy.add_llama(llama2)


def serialize_map(llama_map: List[List[MapGridItem]]):
    """
    Serialize the map to a list of lists of strings
    """
    matrix = llama_map.matrix
    serialized_matrix = []
    for row in matrix:
        serialized_row = []
        for color in row:
            serialized_row.append(color.value if isinstance(color, Enum) else color)
        serialized_matrix.append(serialized_row)
    return {"matrix": serialized_matrix}


game_map = Map(matrix=MAP)

router = APIRouter(prefix="/llama", tags=["llama"])


@router.post(
    path="",
    summary="Create a new llama",
    description="Create a new playable llama",
    operation_id="create_llama",
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {}},
            "description": "Returns a llama to play with.",
        },
    },
)
async def create_lama(llama: LlamaInput = Body(description="Something")) -> Llama:
    """
    Create a new llama
    """
    new_llama = llamas_dummy.add_llama(llama)
    await manager.broadcast(
        json.dumps(
            {
                "event": "create",
                "data": new_llama.dict(),
                "map": serialize_map(game_map),
            }
        )
    )
    return new_llama


@router.get(
    path="/{llama_id}",
    summary="Get llama",
    description="Get llama by an id",
    operation_id="get_llama_by_id",
)
async def get_llama(llama_id: int = Path(description="A llama's id", example=123)) -> Llama:
    """
    Get llama by an id
    """
    llama = llamas_dummy.get_llama(llama_id)
    if llama:
        return llama
    
    raise HTTPException(status_code=400, detail="Provide ID for a llama")


@router.post(
    path="/{llama_id}/step",
    tags=["llama"],
    summary="Move llama",
    description="Move a llama up, down, left or right by a positive number of steps",
    operation_id="add_steps",
)
async def add_steps(
    llama_id: int = Path(description="A llama's id", example=123),
    direction: Direction = Query(
        description="The direction you want the llama to move"
    ),
    steps: int = Query(description="The number of steps to make", example=3),
) -> StepResult:
    """
    Move a llama up, down, left or right by a positive number of steps.
    This adds the steps to the instructions, and they will be executed when the move endpoint is called.
    """
    if steps < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid amount of steps. Steps must be a positive number.",
        )
    llama = llamas_dummy.get_llama(llama_id=llama_id)
    if llama is None:
        raise HTTPException(status_code=404, detail="Llama not found by ID")
    if direction not in Direction.list():
        raise HTTPException(status_code=400, detail="Invalid direction")

    llama.steps_list.append(convert_step_to_coordination(direction, steps))
    await manager.broadcast(
        json.dumps(
            {
                "event": "step",
                "data": {"llama_id": llama_id, "direction": direction, "steps": steps},
            }
        )
    )

    return {"llama_id": llama_id, "direction": direction, "steps": steps}


@router.post(
    path="/{llama_id}/move",
    tags=["llama"],
    summary="Move llama",
    description="Move a llama up, down, left or right by a positive number of steps",
    operation_id="move_llama",
)
async def move_llama(
    llama_id: int = Path(description="A llama's id", example=123)
) -> MoveResult:
    """
    Move the llama following the step instructions previously added.
    """
    llama = llamas_dummy.get_llama(llama_id=llama_id)
    if llama is None:
        raise HTTPException(status_code=404, detail="Llama not found by ID")
    new_steps_list = []
    game_map = Map(matrix=MAP)
    for step in llama.steps_list:
        res = game_map.update_map(step, llama.curr_coordinates)
        llama.curr_coordinates = res["position"]
        llama.add_score(res["score"])
        llama.status = res["status"]
        if llama.status == LlamaStatus.ALIVE:
            new_steps_list.append(step)
        if llama.status == LlamaStatus.DEAD:
            if step[0] != 0:
                final_position = [step[0], 0]
                new_steps_list.append(final_position)
            elif step[1] != 0:
                final_position = [0, step[1]]
                new_steps_list.append(final_position)
            break

    llama.steps_list = new_steps_list
    await manager.broadcast(json.dumps({"event": "move", "data": llama.dict()}))
    return {
        "llama_id": llama_id,
        "score": llama.score,
        "status": llama.status,
        "position": llama.curr_coordinates,
    }
