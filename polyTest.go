package main

import (
	"fmt"
)


type Shape interface {
	corners()	int
}

type Square struct {
	edges	int
}
func (s *Square) corners() int {
	return s.edges
}

type Triangle struct {
	edges	int
}
func (t *Triangle) corners() int {
	return t.edges
}

type ToyBox struct {
	shapes	[]Shape
}
func (t *ToyBox) addShape(s Shape) {
	t.shapes = append(t.shapes, s)
}
type SmallToyBox struct {
	ToyBox
	size	string
}

func main() {
	b := new (SmallToyBox)
	t := new (Triangle)
	t.edges = 3
	s := new (Square)
	s.edges = 4
	b.addShape(s)
	fmt.Println("Square:    ", s.corners())
	fmt.Println("Triangle:  ", t.corners())
	s.edges = 5
	fmt.Println("In ToyBox: ", b.shapes[0].corners())
}