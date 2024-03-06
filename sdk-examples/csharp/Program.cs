// An example of programming against the llama SDK challenge game in C#

using LlamaGame;
using LlamaGame.Models;

// Create the SDK client
var client = new LlamaGameClient();

// Create a llama - for this we need a llama input
// In this example, use libby the liblab llama
var input = new LlamaInput("libby the llama", LlamaColor.White);
var llama = await client.Llama.CreateLlamaAsync(input);

Console.WriteLine($"Created llama {llama.LlamaId}");

// Build a list of moves for the llama

// Down 1
await client.Llama.AddStepsAsync(llama.LlamaId, Direction.Down, 1);

// Right 5
await client.Llama.AddStepsAsync(llama.LlamaId, Direction.Right, 5);

// Down 1
await client.Llama.AddStepsAsync(llama.LlamaId, Direction.Down, 1);

// Now we have the steps, run the moves and print the result
var result = await client.Llama.MoveLlamaAsync(llama.LlamaId);

Console.WriteLine($"Llama {llama.Name} is {result.Status}");
Console.WriteLine($"Score: {result.Score}");
