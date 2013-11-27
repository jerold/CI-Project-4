package quadTree

import (
	"bytes"
	"fmt"
	"math"
	"math/rand"
	// "strconv"
)

// ----- Point ----------------------------------------------------------------------
// ----------------------------------------------------------------------------------

type Point2D interface {
	GetX() float64
	GetY() float64
	Move(dx, dy float64)
	MoveTo(x, y float64)
	Dist(p Point2D) float64
}
type Point struct {
	x float64
	y float64
	z float64
}

func MakePoint(x, y float64) (p Point) { // Public Function \\
	p.initPoint(x, y)
	return p
}
func (p *Point) initPoint(x, y float64) {
	p.x = x
	p.y = y
}
func (p *Point) GetX() float64 { // Public Function \\
	return p.x
}
func (p *Point) GetY() float64 { // Public Function \\
	return p.y
}
func (p *Point) Move(dx, dy float64) { // Public Function \\
	p.x += dx
	p.y += dy
}
func (p *Point) MoveTo(x, y float64) { // Public Function \\
	p.x = x
	p.y = y
}
func (p *Point) Dist(q Point2D) float64 { // Public Function \\
	return math.Sqrt((math.Pow(p.GetX()-q.GetX(), 2) + math.Pow(p.GetY()-q.GetY(), 2)))
}

// ----- Quad Tree ------------------------------------------------------------------
// ----------------------------------------------------------------------------------

var qt QuadTree

type QuadTree struct {
	root     *QuadTree
	depth    int
	maxDepth int

	minPoint Point
	maxPoint Point
	center   Point

	children    []QuadTree
	hasChildren bool

	maxActors  int
	minActors  int
	actors     []Actor
	actorCount int
}

// The Quad Tree effectively manages proximity calculations, reducing the number of distance comparisons
// performed when actors move throughout a 2D space. Quads divide themselves once they reach a given actor
// saturation, limiting the number of actors that any one quad is responsible for at a given time.
func MakeQuad(minPoint Point, maxPoint Point, currentDepth int) (q QuadTree) { // Public Function \\
	q.maxDepth = 12
	q.depth = currentDepth

	q.minPoint = minPoint
	q.maxPoint = maxPoint
	q.center = MakePoint((minPoint.x+maxPoint.x)/2, (minPoint.y+maxPoint.y)/2)

	q.clearChildren()
	q.hasChildren = false

	q.maxActors = 6
	q.minActors = 3
	q.collectActors()
	q.actorCount = 0
	return q
}
func (q *QuadTree) fileActor(a Actor, doAdd bool) {
	q.fileActorAtPosition(a, a.GetPoint(), doAdd)
}

// If the actor is within a child's bounds file it accordingly
func (q *QuadTree) fileActorAtPosition(a Actor, p Point, doAdd bool) {
	for x := 0; x < 2; x++ {
		if x == 0 {
			if p.GetX()-a.GetVisualRange() > q.center.x {
				continue
			}
		} else if p.GetX()+a.GetVisualRange() < q.center.x {
			continue
		}
		for y := 0; y < 2; y++ {
			if y == 0 {
				if p.GetY()-a.GetVisualRange() > q.center.y {
					continue
				}
			} else if p.GetY()+a.GetVisualRange() < q.center.y {
				continue
			}
			if doAdd {
				q.children[x*2+y].AddActor(a)
			} else {
				q.children[x*2+y].removeActorAtPosition(a, p)
			}
		}
	}
}

// New actor or updated actor add actor of split quad and file
func (q *QuadTree) AddActor(a Actor) { // Public Function \\
	q.actorCount++
	if !q.hasChildren && q.depth < q.maxDepth && q.actorCount > q.maxActors {
		q.haveChildren()
	}
	if q.hasChildren {
		q.fileActor(a, true)
	} else {
		q.addActorToActors(a)
	}
}

// Actor will be maintained here in this quad for now
func (q *QuadTree) addActorToActors(a Actor) {
	inActors := false
	for _, actor := range q.actors {
		if actor.GetID() == a.GetID() {
			inActors = true
		}
	}
	if !inActors {
		q.actors = append(q.actors, a)
	}
	q.updateActorNeighbors(a)
}
func (q *QuadTree) RemoveActor(a Actor) { // Public Function \\
	q.removeActorAtPosition(a, a.GetPoint())
}

// Control depth by collecting actors and killing children if required
func (q *QuadTree) removeActorAtPosition(a Actor, p Point) {
	q.actorCount--
	if q.hasChildren && q.actorCount < q.maxActors {
		q.killChildren()
	}
	if q.hasChildren {
		q.fileActorAtPosition(a, p, false)
	} else {
		q.removeActorFromActors(a)
	}
}

// Actor will be removed if it exists in actors"
func (q *QuadTree) removeActorFromActors(a Actor) {
	inActors := false
	index := 0
	for i, actor := range q.actors {
		if actor.GetID() == a.GetID() {
			inActors = true
			index = i
		}
	}
	if inActors {
		newActors := make([]Actor, 0)
		for _, actor := range q.actors[:index] {
			newActors = append(newActors, actor)
		}
		for _, actor := range q.actors[index+1:] {
			newActors = append(newActors, actor)
		}
		q.actors = newActors
	}
	q.updateActorNeighbors(a)
}

// Each time an actor moves we pull it out of the quadtree and replace it to maintained
// Quad Tree simplicity.  The Actor's previous location is used for removal because the Quad's
// state, and neighbor information depends on that information.
func (q *QuadTree) ActorMoved(a Actor, p Point) { // Public Function \\
	q.removeActorAtPosition(a, p)
	q.AddActor(a)
}

// Recheck that all neighbors are still in range
func (q *QuadTree) updateActorNeighbors(a Actor) {
	neighbors := a.GetNeighbors()
	for _, neighbor := range neighbors {
		dist := a.Dist(neighbor)
		if dist > neighbor.GetVisualRange() {
			neighbor.RemoveNeighbor(a)
		}
		if dist > a.GetVisualRange() {
			a.RemoveNeighbor(neighbor)
			q.updateActorNeighbors(a)
			return
		}
	}
	for _, actor := range q.actors {
		if actor.GetID() != a.GetID() {
			dist := a.Dist(actor)
			if dist <= actor.GetVisualRange() {
				actor.AddNeighbor(a)
			} else {
				actor.RemoveNeighbor(a)
			}
			if dist <= a.GetVisualRange() {
				a.AddNeighbor(actor)
			} else {
				a.RemoveNeighbor(actor)
			}
		}
	}
}

// At a given saturation the Quad destributes it's Actors to 4 new children
func (q *QuadTree) haveChildren() {
	childMin := MakePoint(0.0, 0.0)
	childMax := MakePoint(0.0, 0.0)
	q.clearChildren()
	for x := 0; x < 2; x++ {
		if x == 0 {
			childMin.x = q.minPoint.x
			childMax.x = q.center.x
		} else {
			childMin.x = q.center.x
			childMax.y = q.maxPoint.x
		}
		for y := 0; y < 2; y++ {
			if x == 0 {
				childMin.y = q.minPoint.y
				childMax.y = q.center.y
			} else {
				childMin.y = q.center.y
				childMax.y = q.maxPoint.y
			}
			newChild := MakeQuad(childMin, childMax, q.depth+1)
			q.children = append(q.children, newChild)
		}
	}
	for _, actor := range q.actors {
		q.fileActor(actor, true)
	}
	q.clearActors()
	q.hasChildren = true
}

// Performed when there are not enough Children maintained by the Quad's children
// to justify have children, we collect child actors and later delete the children
func (q *QuadTree) collectActors() {
	if q.hasChildren {
		for i := 0; i < 4; i++ {
			q.children[i].collectActors()
			for _, childActor := range q.children[i].actors {
				q.addActorToActors(childActor)
			}
		}
	}
}

// Every parent dreams of outliving their children. Today is not that day
func (q *QuadTree) killChildren() {
	q.collectActors()
	q.clearChildren()
	q.hasChildren = false
}

// Cleanup method to make sure no ghosts remain to haunt us
func (q *QuadTree) clearChildren() {
	q.children = make([]QuadTree, 0, 4)
}

// Cleanup method to make sure no ghosts remain to haunt us
func (q *QuadTree) clearActors() {
	q.actors = make([]Actor, 0, q.maxActors)
}
func (q *QuadTree) PrintQT() string {
	var buffer bytes.Buffer
	buffer.WriteString("[")
	if q.hasChildren {
		for i := 0; i < len(q.children); i++ {
			buffer.WriteString(q.children[i].PrintQT())
		}
	} else {
		for i := 0; i < len(q.actors); i++ {
			buffer.WriteString("+")
		}
	}
	buffer.WriteString("]")
	str := buffer.String()
	if q.depth == 0 {
		fmt.Println(str)
	}
	return str
}

// ----- Actor ----------------------------------------------------------------------
// ----------------------------------------------------------------------------------

var actorIdInc = 0

type Actor interface {
	Point2D
	moved(Point)
	GetPoint() Point
	GetID() int
	GetVisualRange() float64
	SetVisualRange(float64)
	AddNeighbor(Actor)
	RemoveNeighbor(Actor)
	GetNeighbors() []Actor
}
type ActorBase struct {
	Point
	xMax            float64
	yMax            float64
	id              int
	visualRange     float64
	neighbors       []Actor
	maxMemory       int
	memory          []Actor
	neighborsByType map[string][]Actor
	highestDensity  int
}

// When moved an Actor informs the Quadtree watching over all Actors so that proximity service
// can be kept current.  Each Actor can have it's own range of vision, and will see only otherwise
// actors that exist within that range.  Such Actors appear in the Neighbors list
func MakeActor(x, y float64) (a ActorBase) { // Public Function \\
	a.initActor(x, y)
	return a
}
func (a *ActorBase) initActor(x, y float64) {
	a.initPoint(x, y)
	a.xMax = 100
	a.yMax = 100
	if qt.maxDepth == 0 {
		qt = MakeQuad(MakePoint(0, 0), MakePoint(a.xMax, a.yMax), 0)
	}
	a.id = actorIdInc
	actorIdInc++
	a.visualRange = 0
	a.neighbors = make([]Actor, 0)
	a.maxMemory = 100
	a.memory = make([]Actor, 0, a.maxMemory)
	a.neighborsByType = make(map[string][]Actor)
	a.highestDensity = 0
	qt.AddActor(a)
}

// Hook called at the end of Move and MoveTo
func (a *ActorBase) moved(p Point) {}

// Old position is used to help the Quad Tree chech it's pre-movement state for differences
func (a *ActorBase) Move(dx, dy float64) { // Public Function \\
	previousPoint := a.GetPoint()
	a.x += dx
	a.y += dy

	if a.x > a.xMax {
		a.x -= a.xMax
	} else if a.x < 0 {
		a.x += a.xMax
	}
	if a.y > a.yMax {
		a.y -= a.yMax
	} else if a.y < 0 {
		a.y += a.xMax
	}

	qt.ActorMoved(a, previousPoint)
	a.moved(previousPoint)
}

// Instead of moving by some delta, we move to a specific point
func (a *ActorBase) MoveTo(x, y float64) { // Public Function \\
	previousPoint := a.GetPoint()
	a.x = x
	a.y = y
	qt.ActorMoved(a, previousPoint)
	a.moved(previousPoint)
}
func (a *ActorBase) GetPoint() Point { // Public Function \\
	return MakePoint(a.x, a.y)
}
func (a *ActorBase) GetID() int { // Public Function \\
	return a.id
}
func (a *ActorBase) GetVisualRange() float64 { // Public Function \\
	return a.visualRange
}

// Sometimes a range of vision must be changed after initialization, this is how it's done
func (a *ActorBase) SetVisualRange(inRange float64) { // Public Function \\
	if inRange > a.visualRange {
		a.visualRange = inRange
		qt.ActorMoved(a, a.GetPoint())
	} else {
		qt.RemoveActor(a)
		a.visualRange = inRange
		qt.AddActor(a)
	}
}

// Hook called at the end of AddNeighbor
func (a *ActorBase) neighborAdded(b Actor) {}

// Called in the Quad Tree when this Actor, or one in visual range of it moves in to range
func (a *ActorBase) AddNeighbor(b Actor) { // Public Function \\
	inNeighbors := false
	for _, neighbor := range a.neighbors {
		if neighbor.GetID() == b.GetID() {
			inNeighbors = true
		}
	}
	if !inNeighbors {
		a.neighbors = append(a.neighbors, b)
	}
}

// Hook called at the end of RemoveNeighbor
func (a *ActorBase) neighborRemoved(b Actor) {}

// Called in the Quad Tree when this Actor, or one in visual range of it moves out of range
func (a *ActorBase) RemoveNeighbor(b Actor) { // Public Function \\
	inNeighbors := false
	index := 0
	for i, neighbor := range a.neighbors {
		if neighbor.GetID() == b.GetID() {
			inNeighbors = true
			index = i
		}
	}
	if inNeighbors {
		newNeighbors := make([]Actor, 0)
		for _, neighbor := range a.neighbors[:index] {
			newNeighbors = append(newNeighbors, neighbor)
		}
		for _, neighbor := range a.neighbors[index+1:] {
			newNeighbors = append(newNeighbors, neighbor)
		}
		a.neighbors = newNeighbors
	}
}
func (a *ActorBase) GetNeighbors() []Actor { // Public Function \\
	return a.neighbors
}

// ----- Test Class (Inherits from ActorBase) ---------------------------------------
// ----------------------------------------------------------------------------------

type Ant struct {
	ActorBase
	legs int
}

func MakeAnt(x, y float64) (a Ant) {
	a.initAnt(x, y)
	return a
}
func (a *Ant) initAnt(x, y float64) {
	a.initActor(x, y)
	a.legs = 6
}

// ----- Test Main ------------------------------------------------------------------
// ----------------------------------------------------------------------------------

func main() {
	// Test Distance and Movement
	a := MakeActor(10, 10)
	b := MakeActor(20, 10)
	c := MakeAnt(30, 10)
	d := MakeActor(40, 10)
	fmt.Println(a.GetX())
	fmt.Println((&a).Dist(&b))
	fmt.Println((&a).Dist(&c))
	fmt.Println((&a).Dist(&d))
	for i := 0; i < 20; i++ {
		MakeActor(rand.Float64()*100, rand.Float64()*100)
	}
	for i := 0; i < 20; i++ {
		a.Move(rand.Float64()*30, rand.Float64()*30)
		fmt.Println(a.x, a.y, (&a).Dist(&b))
		qt.PrintQT()
	}
}
