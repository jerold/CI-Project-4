package main

import (
	"fmt"
	"math/rand"
)

var learningRate float64 = 0.5

type Neuron struct {
	Weights []float64
	Inputs  []float64
	Output  float64
}

type Layer struct {
	Layer []Neuron
}

type Network struct {
	Net []Layer
}

func (n *Neuron) initNeuron(data []float64) {
	n.Inputs = make([]float64, len(data))
	copy(n.Inputs, data)
}

func (n *Neuron) initWeights(data [][]float64) {
	index := rand.Intn(len(data))
	copy(n.Weights, data[index])
}

func (net *Network) initNet(numInputs int, numClasses int) {
	net.Net = make([]Layer, 2)
	net.Net[0] = Layer{Layer: make([]Neuron, numInputs)}
	net.Net[1] = Layer{Layer: make([]Neuron, numClasses)}
}

func (net *Network) printNet() {
	for i, layer := range net.Net {
		for j, neuron := range layer.Layer {
			fmt.Println("layer", i, "neuron", j, "weights", neuron.Weights)
		}
	}
}

func (net *Network) compete(vector []float64) (winner int) {
	//for i, n := range net.Net[0].Layer {
	//	n.Output = vector[i]
	//}
	var max float64 = -1.0
	winner = 0
	for i, n := range net.Net[1].Layer {
		var sum float64 = 0.0
		//for j := range n.Weights {
		//	sum += n.Weights[j] * vector[i]
		//}
		sum = calcDistance(n.Weights, vector)
		if sum > max {
			max = sum
			winner = i
		}
	}
	net.Net[1].Layer[winner].updateWeights(winner, vector)
	return
}

func (n *Neuron) updateWeights(class int, vector []float64) {
	//fmt.Println("old weight", n.Weights)
	for i, weight := range n.Weights {
		n.Weights[i] = n.Weights[i] + learningRate*(vector[i]-weight)
	}

}
