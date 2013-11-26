package main

import (
	"container/list"
	"fmt"
	"math"
	"math/rand"
)

type Point3D struct {
	x	float32
	y	float32
	z	float32
}
func (p *Point) move(dx, dy float32) {
	p.x += dx
	p.y += dy
}
func (p *Point) moveTo(x, y float32) {
	p.x := x
	p.y := y
}
func (p *Point) dist(q *Point) (distance float32) {
	return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)
}