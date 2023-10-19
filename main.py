
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import routers.llama as llama
import routers.hack as hack
from models.llama import LlamaInput
from connection_manager import manager

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


app = FastAPI(openapi_tags=tags_metadata)


@app.get("/",include_in_schema=False)
async def root():
    return HTMLResponse(html)

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
