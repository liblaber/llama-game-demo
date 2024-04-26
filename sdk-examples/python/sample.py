"""
An example of programming against the llama SDK challenge game in Python
"""
from llama_game import LlamaGame
from llama_game.models import Direction, LlamaColor, LlamaInput

# Create the SDK client
lama_game_client = LlamaGame()

# Create a llama - for this we need a llama input
# In this example, use libby the liblab llama
llama_input = LlamaInput(
    name="libby the llama",
    color=LlamaColor.WHITE,
)

# Create the llama
llama = lama_game_client.llama.create_llama(llama_input)
print(f"Create llama {llama.llama_id}")

# Build a list of moves for the llama

# Down 1
lama_game_client.llama.add_steps(
    steps=1, direction=Direction.DOWN, llama_id=llama.llama_id
)

# Right 5
lama_game_client.llama.add_steps(
    steps=5, direction=Direction.RIGHT, llama_id=llama.llama_id
)

# Down 1
lama_game_client.llama.add_steps(
    steps=1, direction=Direction.DOWN, llama_id=llama.llama_id
)

# Now we have the steps, run the moves and print the result
result = lama_game_client.llama.move_llama(llama_id=llama.llama_id)
print(f"Llama {llama.name} is {result.status}")
print(f"Score: {result.score}")
