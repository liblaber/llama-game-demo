"""
The llama game API
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import llama, hack
from models.llama import LlamaInput
from connection_manager import manager

from dummy import LlamaDummy

# pylint: disable=duplicate-code
llamas_dummy = LlamaDummy()
llama1 = LlamaInput(name="libby")
llamas_dummy.add_llama(llama1)
llama2 = LlamaInput(name="libby2", color="black")
llamas_dummy.add_llama(llama2)


tags_metadata = [
    {
        "name": "hack",
        "description": "Get access to liblab's high score",
    },
    {
        "name": "llama",
        "description": "Control your llama",
    },
]

app = FastAPI(
    title="liblab Llama SDK Challenge",
    servers=[{"url": "http://localhost:8000", "description": "Prod"}],
    contact={"name": "liblab", "url": "https://liblab.com"},
    openapi_tags=tags_metadata,
    description="""
        Welcome to the Llama game! Your purpose is to not hit anything, collect as many coins, 
        and get as far as you can through the maze!
        To play you need to create a Llama with a name and a color, add your steps one by one,
        and then move the Llama and see how far you got! Good luck!
        """,
)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    Define a websocket endpoint for the API
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


app.include_router(llama.router)
app.include_router(hack.router)


def fix_openapi_spec(app_to_fix: FastAPI) -> None:
    """
    The default OpenAPI spec created by FastAPI has trailing slashes on the server URLs.
    This function removes them, as this is a validation error in the spectral analysis of the OpenAPI spec.
    See this discussion from the FastAPI GitHub repo: https://github.com/tiangolo/fastapi/discussions/10309

    This also adds bearer auth to the security schemes and the top level security section
    """
    # Get the existing schema
    existing_schema = app_to_fix.openapi()

    # Remove the trailing slash from the server URL
    for server in existing_schema["servers"]:
        server["url"] = server["url"].rstrip("/")

    # Set the new schema
    app_to_fix.openapi_schema = existing_schema

    # Define a function to return the new schema - the function on the app is replaced with this one
    def get_openapi_schema():
        """
        Return the new schema.
        """
        return existing_schema

    # Replace the function on the app to return the new schema
    app_to_fix.openapi = get_openapi_schema


# Tweak the OpenAPI spec
fix_openapi_spec(app)


@app.get("/", include_in_schema=False)
async def read_root():
    """
    Return the index.html file
    """
    file_path = Path("public/index.html")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="text/html")


app.mount("/", StaticFiles(directory="public"), name="static")
