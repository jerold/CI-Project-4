package main

import (
	"fmt"
	"math/rand"
	"vectorOperations"
)

// adjust the step size for learning
var learningRate float64 = 1

//neuron "class"
type Neuron struct {
	Weights []float64
	Inputs  []float64
	Output  float64
}

//layer "class"
type Layer struct {
	Layer []Neuron
}

//network "class"
type Network struct {
	Net []Layer
}

//init a neuron
func (n *Neuron) initNeuron(data []float64) {
	n.Inputs = make([]float64, len(data))
	copy(n.Inputs, data)
}

//init the weights to a member of the data
func (n *Neuron) initWeights(data [][]float64) {
	index := rand.Intn(len(data))
	copy(n.Weights, data[index])
}

//init the network
func (net *Network) initNet(numInputs int, numClasses int) {
	net.Net = make([]Layer, 2)
	net.Net[0] = Layer{Layer: make([]Neuron, numInputs)}
	net.Net[1] = Layer{Layer: make([]Neuron, numClasses)}
}

//used during testing and debugging. prints a representation of the network
func (net *Network) printNet() {
	for i, layer := range net.Net {
		for j, neuron := range layer.Layer {
			fmt.Println("layer", i, "neuron", j, "weights", neuron.Weights)
		}
	}
}

//basically feed forward. Give the net a data vector
func (net *Network) compete(vector []float64) (winner int) {
	var min float64 = 1 << 63
	winner = 0
	for i, n := range net.Net[1].Layer {
		var sum float64 = 0.0
		sum = vectorOperations.CalcDistance(n.Weights, vector)
		if sum < min {
			min = sum
			winner = i
		}
	}
	net.Net[1].Layer[winner].updateWeights(winner, vector)
	return
}

//update the winning neuron's weights
func (n *Neuron) updateWeights(class int, vector []float64) {
	for i, weight := range n.Weights {
		n.Weights[i] = n.Weights[i] + learningRate*(vector[i]-weight)
	}

}

//that was easy!
