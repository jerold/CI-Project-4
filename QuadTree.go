package main

import (
	"fmt"
	"math"
	//"math/rand"
)



// ----- Point ----------------------------------------------------------------------

type Movable interface {
	GetX() float64
	GetY() float64
	Move(dx, dy float64)
	MoveTo(x, y float64)
}
type Point struct {
	x	float64
	y	float64
	z	float64
}
func MakePoint(x, y float64) (p Point) {
	p.InitPoint(x, y)
	return p
}
func (p *Point) InitPoint(x, y float64) {
	p.x = x
	p.y = y
}
func (p *Point) GetX() (float64) {
	return p.x
}
func (p *Point) GetY() (float64) {
	return p.y
}
func (p *Point) Move(dx, dy float64) {
	p.x += dx
	p.y += dy
}
func (p *Point) MoveTo(x, y float64) {
	p.x = x
	p.y = y
}
func (p *Point) Dist(q Movable) float64 {
	return math.Sqrt((math.Pow(p.GetX() - q.GetX(), 2) + math.Pow(p.GetY() - q.GetY(), 2)))
}



// ----- Quad Tree ------------------------------------------------------------------

var qt QuadTree

type QuadTree struct {
	root			*QuadTree
	depth			int
	maxDepth		int

	minPoint		Point
	maxPoint		Point
	center			Point

	children		[]QuadTree
	hasChildren		bool

	maxActors		int
	minActors		int
	actors			[]Actor
	actorCount		int
}
func MakeQuad(minPoint Point, maxPoint Point, currentDepth int) (q QuadTree) {
	q.maxDepth = 6
	q.depth = currentDepth

	q.minPoint = minPoint
	q.maxPoint = maxPoint
	q.center = MakePoint((minPoint.x+maxPoint.x)/2, (minPoint.y+maxPoint.y)/2)

	q.children = make([]QuadTree, 4)
	q.hasChildren = false

	q.maxActors = 6
	q.minActors = 3
	q.actors = make([]Actor, q.maxActors)
	q.actorCount = 0
	return q
}



// ----- Actor ----------------------------------------------------------------------

var actorIdInc = 0

type HasNeighbors interface {
	GetID() int
	AddNeighbor(b *Actor)
	RemoveNeighbor(b *Actor)
}
type Actor struct {
	Point
	xMax			float64
	yMax			float64
	id				int
	rangeOfVision	float64
	neighbors		[]*Actor
	maxMemory		int
	memory			[]*Actor
	neighborsByType	map[string][]Actor
	highestDensity	int
}
func MakeActor(x, y float64) (a Actor) {
	a.InitActor(x, y)
	return a
}
func (a *Actor) InitActor(x, y float64) {
	a.InitPoint(x, y)
	a.xMax = 100
	a.yMax = 100
	if qt.maxDepth == 0 {
		qt = MakeQuad(MakePoint(0, 0), MakePoint(a.xMax, a.yMax), 0)
	}
	a.id = actorIdInc
	actorIdInc++
	a.rangeOfVision = 2
	a.neighbors = make([]*Actor, 0)
	a.maxMemory = 100
	a.memory = make([]*Actor, 0, a.maxMemory)
	a.neighborsByType = make(map[string][]Actor)
	a.highestDensity = 0
}
func (a *Actor) GetID() int {
	return a.id
}
func (a *Actor) AddNeighbor(b *Actor) {
	inNeighbors := false
	for i := range a.neighbors {
		if a.neighbors[i].id == b.GetID() {
			inNeighbors = true
		}
	}
	if !inNeighbors {
		a.neighbors = append(a.neighbors, b)
	}
}
func (a *Actor) RemoveNeighbor(b *Actor) {
	inNeighbors := false
	index := 0
	for i := range a.neighbors {
		if a.neighbors[i].id == b.GetID() {
			inNeighbors = true
			index = i
		}
	}
	if inNeighbors {
		newNeighbors := make([]*Actor, 0)
		for i := range a.neighbors[:index] {
			newNeighbors = append(newNeighbors, a.neighbors[:index][i])
		}
		for i := range a.neighbors[index+1:] {
			newNeighbors = append(newNeighbors, a.neighbors[index+1:][i])
		}
		a.neighbors = newNeighbors
	}
}

type Ant struct {
	Actor
	legCount	int
}
func MakeAnt(x, y float64) (a Ant) {
	a.Init(x, y)
	a.legCount = 6
	return a
}
func main() {
	// Test Distance and Movement
	a := MakeActor(10, 10)
	b := MakeActor(20, 10)
	c := MakeAnt(30, 10)
	d := MakeActor(40, 10)
	fmt.Println(a.Dist(&b))
	a.Move(5, 0)
	b.MoveTo(15, 20)
	fmt.Println(a.Dist(&b))

	// Test Neightbor Adding and Removing
	a.AddNeighbor(&b)
	a.AddNeighbor(&c)
	a.AddNeighbor(&d)
	fmt.Println(len(a.neighbors))
	a.RemoveNeighbor(&c)
	fmt.Println(len(a.neighbors))
}