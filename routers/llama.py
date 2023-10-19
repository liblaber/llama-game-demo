import json
from fastapi import APIRouter, HTTPException, Query, Body, Path, status
from dummy import LlamaDummy
from models.llama import LlamaInput, Llama
from models.common import Direction
from game_logic.maps import MAP, Map, LlamaStatus
from game_logic.calculations import convert_step_to_coordination
from connection_manager import manager


# for testing
llamas_dummy = LlamaDummy()
llama1 = LlamaInput(name="libby")
llamas_dummy.add_llama(llama1)
llama2 = LlamaInput(name="libby2", color="black")
llamas_dummy.add_llama(llama2)


game_map = Map(matrix=MAP)

router = APIRouter(prefix='/llama', tags=[ "llama"] )

@router.post(
    path="/", 
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
    new_llama = llamas_dummy.add_llama(llama)
    await manager.broadcast(json.dumps({"event": "create", "data": new_llama.dict(), "map": game_map}))
    new_llama.steps_list.append(new_llama.start_coordinates)
    return new_llama

@router.get(
    path="/{id}", 
    summary="Get llama", 
    description="Get llama by an id", 
    operation_id="get_llama_by_id")
async def get_llama(id: int = Path(description="A llama's id")) -> Llama:
    llama = llamas_dummy.get_llama(id)
    if llama:
        return llama 
    else:
        raise HTTPException(status_code=400, detail="Provide ID for a llama")


@router.post(
    path="/{id}/step", 
    tags=["llama"], 
    summary="Move llama", 
    description="Move a llama up, down, left or right by a positive number of steps", 
    operation_id="add_steps"
    )
async def add_steps(id: int = Path(description="A llama's id"), direction: Direction = Query(description="The direction you want the llama to move"), steps: int= Query(description="The number of steps to make")):
    if steps < 0:
        raise HTTPException(status_code=400, detail="Invalid amount of steps. Steps must be a positive number.")
    llama = llamas_dummy.get_llama(id=id)
    if llama is None:
        raise HTTPException(status_code=404, detail="Llama not found by ID")
    if direction not in Direction.list():
        raise HTTPException(status_code=400, detail="Invalid direction")

    llama.steps_list.append(convert_step_to_coordination(direction, steps))
    await manager.broadcast(json.dumps({"event": "move","data":{"id": id, "direction": direction, "steps": steps}}))

    return {"id": id, "direction": direction, "steps": steps}

@router.post(
    path="/{id}/move", 
    tags=["llama"], 
    summary="Move llama", 
    description="Move a llama up, down, left or right by a positive number of steps", 
    operation_id="move_llama"
    )
async def move_llama(id: int = Path(description="A llama's id")):
    llama = llamas_dummy.get_llama(id=id)
    if llama is None:
        raise HTTPException(status_code=404, detail="Llama not found by ID")

    for step in llama.steps_list:
        res = game_map.update_map(step, llama.curr_coordinates)
        llama.curr_coordinates = res["position"]
        llama.add_score(res["score"])
        llama.status = res["status"]
        if llama.status == LlamaStatus.DEAD:
            break

    
    await manager.broadcast(json.dumps(llama.dict()))

    return {"id": id, "score": llama.score, "status": llama.status, "position": llama.curr_coordinates }