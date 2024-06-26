// An example of programming against the llama SDK challenge game in Go

package main

import (
	"context"
	"fmt"

	"github.com/liblaber/llama-store-sdk-go/pkg/llama"
	"github.com/liblaber/llama-store-sdk-go/pkg/llamagame"
	"github.com/liblaber/llama-store-sdk-go/pkg/llamagameconfig"
)

func main() {
	// Create the SDK client
	config := llamagameconfig.NewConfig()
	llamaGameClient := llamagame.NewLlamaGame(config)

	// Create a llama - for this we need a llama input
	// In this example, use libby the liblab llama
	llamaInput := llama.LlamaInput{}
	llamaInput.SetName("libby the llama")
	llamaInput.SetColor(llama.LLAMA_COLOR_WHITE)

	// Create the llama
	newLlama, _ := llamaGameClient.Llama.CreateLlama(context.Background(), llamaInput)
	fmt.Printf("Created llama %d\n", *newLlama.Data.LlamaId)

	// Build a list of moves for the llama

	// Down 1
	addSteps := llama.AddStepsRequestParams{}
	addSteps.SetDirection(llama.DIRECTION_DOWN)
	addSteps.SetSteps(1)

	llamaGameClient.Llama.AddSteps(context.Background(), *newLlama.Data.LlamaId, addSteps)

	// Right 5
	addSteps.SetDirection(llama.DIRECTION_RIGHT)
	addSteps.SetSteps(5)

	llamaGameClient.Llama.AddSteps(context.Background(), *newLlama.Data.LlamaId, addSteps)

	// Down 1
	addSteps.SetDirection(llama.DIRECTION_DOWN)
	addSteps.SetSteps(1)

	llamaGameClient.Llama.AddSteps(context.Background(), *newLlama.Data.LlamaId, addSteps)

	// Now we have the steps, run the moves and print the result
	result, _ := llamaGameClient.Llama.MoveLlama(context.Background(), *newLlama.Data.LlamaId)
	fmt.Printf("Llama %s is %s\n", *newLlama.Data.Name, *result.Data.Status)
	fmt.Printf("Score: %d\n", *result.Data.Score)
}
