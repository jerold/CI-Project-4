from math import sqrt


class Point:
	def __init__(self, inX, inY):
		self.x = inX
		self.y = inY

	def move(self, dX, dY):
		self.x = self.x + dX
		self.y = self.y + dY

	def dist(self, p2):
		dx = self.x - p2.x
		dy = self.y - p2.y
		return sqrt(dx**2 + dy**2)


class QuadTree(object):
	maxDepth = 6;
	minActorsPerQuadTree = 3;
	maxActorsPerQuadTree = 6;

	def __init__(self, minPoint, maxPoint, currentDepth):
		self.minPoint = minPoint;
		self.maxPoint = maxPoint;
		self.center = Point((minPoint.x+maxPoint.x)/2, (minPoint.y+maxPoint.y)/2);
		self.children = [];
		self.hasChildren = False;
		self.actors = [];
		self.depth = currentDepth;
		self.numberOfActors = 0;

	def width(self):
		return self.maxPoint.x - self.minPoint.x

	def height(self):
		return self.maxPoint.x - self.minPoint.x

	def center(self):
		return self.center

	def fileActor(self, actor, doAdd):
		self.fileActorAtPosition(actor, actor.position, doAdd)

	def fileActorAtPosition(self, actor, position, doAdd):
		"""if the actor is within a child's bounds file it accordingly"""
		for x in range(2):
			if x == 0:
				if position.x - actor.rangeOfVision > self.center.x:
					continue
			elif position.x + actor.rangeOfVision < self.center.x:
				continue
			for y in range(2):
				if y == 0:
					if position.y - actor.rangeOfVision > self.center.y:
						continue
				elif position.y + actor.rangeOfVision < self.center.y:
					continue
				if doAdd:
					self.children[x][y].addActor(actor)
				else:
					self.children[x][y].removeActorAtPosition(actor, position)

	def addActor(self, actor):
		"""new actor or updated actor add actor of split quad and file"""
		self.numberOfActors = self.numberOfActors + 1
		if not self.hasChildren and self.depth < QuadTree.maxDepth and self.numberOfActors > QuadTree.maxActorsPerQuadTree:
			self.haveChildren()
		if self.hasChildren:
			self.fileActor(actor, True)
		else:
			self.addActorToActors(actor)

	def addActorToActors(self, actor):
		"""actor will be put here in this quad"""
		if actor not in self.actors:
			self.actors.append(actor)
			self.updateActorNeighbors(actor)

	def removeActor(self, actor):
		self.removeActorAtPosition(actor, actor.position)

	def removeActorAtPosition(self, actor, position):
		"""control depth by collecting actors and killing children if required"""
		self.numberOfActors = self.numberOfActors - 1
		if self.hasChildren and self.numberOfActors < QuadTree.minActorsPerQuadTree:
			self.killChildren()
		if self.hasChildren:
			self.fileActorAtPosition(actor, position, False)
		else:
			self.removeActorFromActors(actor)

	def removeActorFromActors(self, actor):
		if actor in self.actors:
			self.actors.remove(actor)
			self.updateActorNeighbors(actor)

	def actorMoved(self, actor, fromPosition):
		self.removeActorAtPosition(actor, fromPosition)
		self.addActor(actor)

	def updateActorNeighbors(self, actor):
		"""Recheck that all neighbors are still in range"""
		for neighbor in actor.neighbors:
			dist = actor.dist(neighbor)
			# remove actor from neightbor if actor is out of their range
			if dist > neighbor.rangeOfVision:
				neighbor.removeNeighbor(actor)
			# Remove neighbor from actor if neighbor is out of actor's range
			if dist > actor.rangeOfVision:
				actor.removeNeighbor(neighbor)
				self.updateActorNeighbors(actor)
				return
		for potentialNeighbor in self.actors:
			if actor is not potentialNeighbor:
				dist = actor.dist(potentialNeighbor)
				# try to add actor to neighbor if in range otherwise try to remove
				if dist <= potentialNeighbor.rangeOfVision:
					potentialNeighbor.addNeightbor(actor)
				else:
					potentialNeighbor.removeNeighbor(actor)
				# try to add neighbor to actor if in range otherwise try to remove
				if dist <= actor.rangeOfVision:
					actor.addNeightbor(potentialNeighbor)
				else:
					actor.removeNeighbor(potentialNeighbor)

	def haveChildren(self):
		childMin = Point(0.0, 0.0)
		childMax = Point(0.0, 0.0)
		self.clearChildren()
		for x in range(2):
			if x == 0:
				childMin.x = self.minPoint.x
				childMax.x = self.center.x
			else:
				childMin.x = self.center.x
				childMax.y = self.maxPoint.x
			for y in range(2):
				if y == 0:
					childMin.y = self.minPoint.y
					childMax.y = self.center.y
				else:
					childMin.y = self.center.y
					childMax.y = self.maxPoint.y
				self.children[x].append(QuadTree(childMin, childMax, self.depth + 1))
		for actor in self.actors:
			self.fileActor(actor, True)
		self.actors = []
		self.hasChildren = True

	def collectActors(self):
		for x in range(2):
			for y in range(2):
				self.children[x][y].collectActors()
				for childActor in self.children[x][y].actors:
					self.addActorToActors(childActor)

	def killChildren(self):
		self.collectActors()
		self.clearChildren()
		self.hasChildren = False

	def clearChildren(self):
		self.children = [[], []]

	def __str__(self):
		out = ""
		for _ in range(self.depth):
			out = out + "  "
		out = out + "["
		if self.hasChildren:
			for x in range(2):
				for y in range(2):
					out = out + "\n" + str(self.children[x][y])
		else:
			for _, a in enumerate(self.actors):
				out = out + "."
		out = out + "]"
		return out


class Actor(object):
	quadTree = QuadTree(Point(0.0, 0.0), Point(100.0, 100.0), 0)
	actorIdInc = 0

	def __init__(self, position):
		self.id = Actor.actorIdInc
		Actor.actorIdInc = Actor.actorIdInc + 1
		self.position = position
		self.rangeOfVision = 0
		self.neighbors = []
		Actor.quadTree.addActor(self)

	def move(self, dX, dY):
		oldPosition = Point(self.position.x, self.position.y)
		self.position.move(dX, dY)
		Actor.quadTree.actorMoved(self, oldPosition)
		# print(str(Actor.quadTree))

	def setRangeOfVision(self, inRange):
		if inRange > self.rangeOfVision:
			self.rangeOfVision = inRange
			Actor.quadTree.actorMoved(self, self.position)
		else:
			Actor.quadTree.removeActor(self)
			self.rangeOfVision = inRange
			Actor.quadTree.addActor(self)

	def getX(self):
		return self.position.x

	def getY(self):
		return self.position.y

	def dist(self, a2):
		return self.position.dist(a2.position)

	def addNeightbor(self, actor):
		if actor not in self.neighbors:
			self.neighbors.append(actor)
			# print("A " + str(self.id) + " : " + ",".join(str(n.id) for n in self.neighbors))

	def removeNeighbor(self, actor):
		if actor in self.neighbors:
			self.neighbors.remove(actor)
			# print("R " + str(self.id) + " : " + ",".join(str(n.id) for n in self.neighbors))