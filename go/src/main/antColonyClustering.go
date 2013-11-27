package main

import (
	//"quadTree.Point"
	//"quadTree.Actor"
	"quadTree"
	//"time"
	//"math/rand"
	//"math"
	"vectorOperations"
)

//Assistance Methods

func addNeighborsToCluster(vector []float64, cluster [][][]float64) {
	
}

//Environment Classes

type Cluster struct {
	Clusters [][][]float64
	OutLayers [][]float64
	HasClusters bool
	Packets []quadTree.Actor
}

type Packet struct {
	Position {quadTree.Actor quadTree.Actor{}}
	Packets []float64
	BaseVariance float64
}

type Pheromone struct {
	Pheromones []quadTree.Actor
}

type Ant struct {
	ants = []quadTree.Actor
}

type Colony struct {
	
}

func (c *Cluster) count (int) {
	return len(c.Packets)
}

func (c *Cluster) percentage (float64) {
	temp := float64(len(c.Packets))/float64(len(Packet.Packets))*100.0
}

func (c *Cluster) variance() ([]float64){
	if len(c.Packets) == 0 {
		return make([]float64, 0)
	}
	return vectorOperations.FindVariance(c.Packets, vectorOperations.FindMean(c.Clusters[0]))
}

func (c *Cluster) types {
	//do nothing for now
	c.Clusters = make([][][]float64, 0)
}

func (c *Cluster) reset {
	c.Clusters = make([][][]float64, 0)
	c.Outlayers = make([][]float64, 0)
	c.HasClusters = false
}

func (p *Packet) update {
	point := &quadTree.Point{p.Position.x, p.Position.y}
