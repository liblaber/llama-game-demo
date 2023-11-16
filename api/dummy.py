from typing import Union
from models.llama import LlamaInput, Llama, LlamaColor


class LlamaDummy:
    def __init__(self):
        self.llamas: Llama = []
        self.latest_id: int = 0

    def get_latest_id(self) -> int:
        return self.latest_id

    def update_latest_id(self) -> int:
        self.latest_id += 1
        return self.latest_id

    def update_llamas(self, llama: Llama) -> None:
        self.llamas.append(llama)

    def get_llama(self, llama_id: int = None) -> Union[None, Llama]:
        if llama_id is not None:
            for llama in self.llamas:
                if llama.llama_id == llama_id:
                    return llama
        return None

    def add_llama(self, llama: LlamaInput) -> Llama:
        llama_dict = llama.dict()
        new_llama = Llama(**llama_dict, llama_id=self.update_latest_id())
        self.update_llamas(new_llama)
        return new_llama

    def update_llama(self, llama_id: int, name: str = None, color: LlamaColor = None):
        found_llama = self.get_llama(llama_id)
        if found_llama:
            if name:
                found_llama.name = name
            if color:
                found_llama.color = color


HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
