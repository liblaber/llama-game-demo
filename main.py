
from fastapi import FastAPI, HTTPException,WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import routers.llama as llama
import routers.hack as hack
from models.llama import LlamaInput
from connection_manager import manager
from pathlib import Path

from dummy import LlamaDummy, html

llamas_dummy = LlamaDummy()
llama1 = LlamaInput(name="libby")
llamas_dummy.add_llama(llama1)
llama2 = LlamaInput(name="libby2", color="black")
llamas_dummy.add_llama(llama2)


tags_metadata = [
    {
        "name": "Hack",
        "description": "Get access to Liblab's high score",
    },
    {
        "name": "llama",
        "description": "Control your llama",
    },
]


app = FastAPI(openapi_tags=tags_metadata, description="""Welcome to the Llama game! Your purpose is to not hit anything, collect as many coins, and get as far as you can through the maze!
To play you need to create a Llama with a name and a color, add your steps one by one, and then move the Llama and see how far you got! Good luck!""")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
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

@app.get("/", include_in_schema=False)
async def read_root():
    file_path = Path("public/index.html")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="text/html")

app.mount("/", StaticFiles(directory="public"), name="static")
