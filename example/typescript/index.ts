// An example of programming against the llama SDK challenge game in TypeScript

import { Llamagame, LlamaInput } from 'llamagame';

const llamaGameClient = new Llamagame();

(async () => {
  // Create a llama - for this we need a llama input
  // In this example, use libby the liblab llama
  const llamaInput: LlamaInput = {
    name: 'libby the llama',
    color: 'white',
  };

  // Create the llama
  const llama = await llamaGameClient.llama.createLlama(llamaInput);
  console.log(`Create llama ${llama.llama_id}`);

  // Build a list of moves for the llama

  // Down 1
  llamaGameClient.llama.addSteps(llama.llama_id, 'down', 1);

  // Right 5
  llamaGameClient.llama.addSteps(llama.llama_id, 'right', 5);

  // Down 1
  llamaGameClient.llama.addSteps(llama.llama_id, 'down', 1);

  // Now we have the steps, run the moves and print the result
  const result = await llamaGameClient.llama.moveLlama(llama.llama_id);
  console.log(`Llama ${llama.name} is ${result.status}`);
  console.log(`Score: ${result.score}`);
})();