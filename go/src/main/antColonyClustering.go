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
	Clusters    [][][]float64
	OutLayers   [][]float64
	HasClusters bool
	Packets     []Packet
}

type Packet struct {
	Position      quadTree.Point2D
	Packets       []Packet
	BaseVariance  float64
	Pattern       []Pattern
	InHand        bool
	hasMembership bool
}

type Pheromone struct {
	Pheromones []Pheromone
}

type Ant struct {
	Ants []Ant
}

type Colony struct {
	Packets []Packet
}

func (c *Cluster) count(temp int) {
	temp = len(c.Packets)
	return
}

func (c *Cluster) percentage(p *Packet) (temp float64) {
	temp = float64(len(c.Packets)) / float64(len(p.Packets)) * 100.0
	return
}

func (c *Cluster) variance() []float64 {
	if len(c.Packets) == 0 {
		return make([]float64, 0)
	}
	return vectorOperations.FindVariance(c.Clusters[0], vectorOperations.FindMean(c.Clusters[0]))
}

func (c *Cluster) types() {
	//do nothing for now
	c.Clusters = make([][][]float64, 0)
}

func (c *Cluster) reset() {
	c.Clusters = make([][][]float64, 0)
	c.OutLayers = make([][]float64, 0)
	c.HasClusters = false
}

func (p *Packet) update() {
	point := &quadTree.Point{p.Position.GetX(), p.Position.GetY(), 0}
	point.Z = 0

}
