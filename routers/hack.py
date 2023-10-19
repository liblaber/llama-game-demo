from fastapi import APIRouter, Query, status

router = APIRouter(prefix='/hack_liblab', tags=[ "hack"] )

@router.post(
    path="/", 
    summary="Hack Liblab", 
    description="Attempt to guess Liblab's admin password.", 
    operation_id="hack_attemp", 
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {}},
            "description": "Hacker man",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid password."},
    },
    )
async def hack_attemp(password: str = Query(description="The password you think we use", example="None of your business")) -> str:
    return {"response": "what did you think was going to happen?"}
