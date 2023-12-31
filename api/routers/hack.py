from fastapi import APIRouter, Query, status
from models.hack import HackResult

router = APIRouter(prefix="/hack_liblab", tags=["hack"])


@router.post(
    path="",
    summary="Hack liblab",
    description="Attempt to guess liblab's admin password.",
    operation_id="hack_attempt",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {}},
            "description": "Hacker man",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid password."},
    },
)
async def hack_attemp(
    # pylint: disable=unused-argument
    password: str = Query(
        description="The password you think we use", example="None of your business"
    )
) -> HackResult:
    return {"response": "what did you think was going to happen?"}
