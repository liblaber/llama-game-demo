from pydantic import BaseModel, Field


class HackResult(BaseModel):
    """
    Hacking result.
    """

    response: str = Field(description="Did you make it?")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "Oh no! You did it! Our systems are down! What are we going to do??",
                }
            ]
        },
        "description": "The results of your hacking.",
        "from_attributes": True,
    }
