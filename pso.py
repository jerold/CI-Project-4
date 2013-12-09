from patternSet import PatternSet
import time
import random
import math
	
def euclidianCopy(p):
	c = []
	for i in p:
		c.append(i)
	return c

def emptyCopy(p):
	c = []
	for i in p:
		c.append(0.0)
	return c

def patternsMean(patterns):
	mean = emptyCopy(patterns[0]['p'])
	for pattern in patterns:
		for i, v in enumerate(pattern['p']):
			mean[i] = mean[i] + v
	for i, v in enumerate(mean):
		mean[i] = v/len(patterns)
	return mean

def patternVarience(p, q):
	"""Combined difference between two vectors"""
	var = 0.0
	for i in range(len(p)):
		var = var + (p[i] - q[i])*(p[i] - q[i])
	return var

def patternsStandardDeviation(patterns, mean):
	varience = emptyCopy(mean)
	for pattern in patterns:
		for j, item in enumerate(pattern['p']):
			varience[j] += pow(item - mean[j], 2)
	for i, v in enumerate(varience):
		varience[i] = math.sqrt(varience[i] / len(patterns))
	return varience

def euclidianDistance(p, q):
	"""Distance function in multi-dimensional space"""
	sumOfSquares = 0.0
	for i in range(len(p)):
		sumOfSquares = sumOfSquares + ((p[i]-q[i])*(p[i]-q[i]))
	return math.sqrt(sumOfSquares)

def standardDeviation(collection):
	"""Basid Standard Deviation helps us determine how scattered the patterns are"""
	if len(collection) > 0:
		average = sum(collection)/len(collection)
		squaredDifferences = 0.0
		for val in collection:
			squaredDifferences = squaredDifferences + (val - average)*(val - average)
		meanSquaredDifference = squaredDifferences/len(collection)
		standardDeviation = math.sqrt(meanSquaredDifference)
		return standardDeviation
	return 999999




class Particle:
	particles = []

	def __init__(self, position):
		self.v = self.initVelocity(position)	# Velocity
		self.x = euclidianCopy(position)		# Position
		self.hx = []							# Position History
		self.fitness = 9999.9					# Fitness
		self.bx = euclidianCopy(position)		# Best
		self.bFitness = 9999.9					# Best Fitness
		self.resetMemberInfo()
		self.pIndex = len(Particle.particles)
		Particle.particles.append(self)
		if self.pIndex == 0:
			Particle.best = self
		self.bestInterMemberDistance = 9999.9
		self.iterationsSinceBestUpdate = 0

	def resetMemberInfo(self):
		self.members = []
		self.memberDistances = []

	def initVelocity(self, position):
		v = []
		for i, _ in enumerate(position):
			v.append(float(random.randrange(-1000, 1000))/3000)
		return v

	def updateFitness(self):
		# minimize inter cluster distance
		if len(self.memberDistances) > 0:
			self.fitness = sum(self.memberDistances)/len(self.memberDistances)	# Reward for being closer to members
			# self.fitness = self.fitness + max(self.memberDistances)

			# maxInterMemberDistance = 0
			# for member1 in self.members:
			# 	for member2 in self.members:
			# 		dist = euclidianDistance(member1['p'], member2['p'])
			# 		if dist > maxInterMemberDistance:
			# 			maxInterMemberDistance = dist
			# if maxInterMemberDistance < self.bestInterMemberDistance:
			# 	self.bestInterMemberDistance = maxInterMemberDistance
			# self.fitness = self.fitness + maxInterMemberDistance
			
			mean = patternsMean(self.members)
			self.fitness = self.fitness + euclidianDistance(self.x, mean)*2		# Reward for centering on cluster

			sd = patternsStandardDeviation(self.members, mean)
			self.fitness = self.fitness + sum(sd)								# Reward for cluster tightness

			# intraClusterComponent = sum(sd)/len(sd)
			# interClusterComponent = patternVarience(self.x, mean)
			# self.fitness = self.fitness + interClusterComponent

			if self.fitness < self.bFitness:
				self.bx = euclidianCopy(self.x)
				self.bFitness = self.fitness
				if self.bFitness < Particle.best.bFitness:
					Particle.best = self
					for p2 in Particle.particles:
						if p2.pIndex != self.pIndex:
							p2.bFitness = 9999.9
				self.iterationsSinceBestUpdate = 0
			else:
				self.iterationsSinceBestUpdate = self.iterationsSinceBestUpdate + 1
		else:
			self.fitness = 9999.9


	def updatePosition(self):
		self.updateV()
		self.updateX()

	def updateV(self):
		nbx = self.neighborhoodBest()
		gbx = self.globalBest()
		anneal = pow(.95, self.iterationsSinceBestUpdate)
		# if self.pIndex == 0:
		# 	print("VB: " + str(self.v))
		# 	print("XB: " + str(self.x))
		# 	print("LX: " + str(self.bx))
		# 	print("NX: " + str(nbx))
		# 	print("GX: " + str(gbx))
		for i, v in enumerate(self.v):
			# self.v[i] = .98*v + .05*(self.bx[i] - self.x[i]) + 0.1*(random.random()-.5)
			# self.v[i] = v + .05*(self.bx[i] - self.x[i]) + .01*(nbx[i] - self.x[i]) + .01*(gbx[i] - self.x[i])
			# self.v[i] = v + .05*(self.bx[i] - self.x[i]) + .01*(nbx[i] - self.x[i])
			# self.v[i] = v + .05*(self.bx[i] - self.x[i]) + .05*(gbx[i] - self.x[i])
			self.v[i] = .98*v + .05*(self.bx[i] - self.x[i]) + anneal*.001*(gbx[i] - self.x[i]) + anneal*0.1*(random.random()-.5)

	def updateX(self):
		# Effectively turns PSO into K-Means
		# mPat = patternsMean(self.members)
		# for i, v in enumerate(self.x):
		# 	self.x[i] = mPat[i]

		# Basid position update
		for i, x in enumerate(self.x):
			self.x[i] = x + self.v[i]
		self.hx.append(euclidianCopy(self.x))

		# if self.pIndex == 0:
		# 	print("F: " + str(self.fitness))
		# 	print("VA: " + str(self.v))
		# 	print("XA: " + str(self.x))


	def neighborhoodBest(self):
		neighborCount = 2
		best = Particle.particles[0]
		for particle in Particle.particles[self.pIndex:(self.pIndex+neighborCount)%len(Particle.particles)]:
			if particle.bFitness < best:
				best = particle
		return best.bx

	def globalBest(self):
		return Particle.best.bx

	def __str__(self):
		s = "P[" + ", ".join(str(x) + ":" + str(round(self.v[i], 3)) for i, x in enumerate(self.x)) + "]"
		return s




class Swarm:
	minV = []
	maxV = []

	def __init__(self, particleCount, patterns):
		self.patterns = []
		for p in patterns:
			self.patterns.append(p)
		self.particles = self.initParticles(particleCount, patterns)
		# patSample = random.sample(self.patterns, particleCount)
		# for p in patSample:
		# 	newPart = Particle(p['p'])
		# 	self.particles.append(newPart)
			# print(newPart)

	def initParticles(self, particleCount, patterns):
		Swarm.minV = euclidianCopy(patterns[0]['p'])
		Swarm.maxV = euclidianCopy(patterns[0]['p'])
		for p in patterns:
			for i, x in enumerate(p['p']):
				if x < Swarm.minV[i]:
					Swarm.minV[i] = x
				if x > Swarm.maxV[i]:
					Swarm.maxV[i] = x
		parts = []
		for i in range(particleCount):
			parts.append(Particle(self.randomPositionInRange()))
		return parts

	def randomPositionInRange(self):
		newPattern = emptyCopy(self.patterns[0]['p'])
		for i, _ in enumerate(newPattern):
			try:
				newPattern[i] = float(random.randrange(int(Swarm.minV[i]*1000), int(Swarm.maxV[i]*1000)))/1000
			except ValueError:
				newPattern[i] = 0.0
		return newPattern

	def update(self):
		self.checkProximity()
		self.updateMembership()
		self.updateParticles()

	def checkProximity(self):
		for p1 in self.particles:
			for p2 in self.particles:
				if p1.pIndex != p2.pIndex and euclidianDistance(p1.bx, p2.bx) < 0.5:
					print("Get out of Here <----------------<<<")
					p1.bFitness = 9999.9
					p1.initVelocity(self.randomPositionInRange())

	def updateMembership(self):
		for particle in self.particles:
			particle.resetMemberInfo()
		for pattern in self.patterns:
			minDist = 99999
			particleIndex = 0
			distances = []
			for i, particle in enumerate(self.particles):
				distances.append(euclidianDistance(particle.x, pattern['p']))
				if distances[-1] < minDist:
					minDist = distances[-1]
					particleIndex = i
			pattern['m'] = particleIndex
			pattern['h'].append(particleIndex)
			self.particles[particleIndex].members.append(pattern)
			self.particles[particleIndex].memberDistances.append(distances[particleIndex])

	def updateParticles(self):
		for particle in self.particles:
			particle.updateFitness()
		for particle in self.particles:
			particle.updatePosition()

	def setParticlesToPersonBest(self):
		for particle in self.particles:
			for i, x in enumerate(particle.x):
				particle.v[i] = particle.x[i] - particle.bx[i]
			particle.updateX()


if __name__=="__main__":
	# Batch: (ordered by least time complex to most)
	# allDataTypes = ['data/iris/iris.json',
	#				 'data/seeds/seeds.json',
	#				 'data/glass/glass.json',
	#				 'data/wine/wine.json',
	#				 'data/zoo/zoo.json',
	#				 'data/heart/heart.json',
	#				 'data/car/car.json',
	#				 'data/yeast/yeast.json',
	#				 'data/block/pageblocks.json',
	#				 'data/ionosphere/ionosphere.json']

	# Single:
	# allDataTypes = ['psoTestSet.json']
	# allDataTypes = ['data/iris/iris.json']
	# allDataTypes = ['data/seeds/seeds.json']
	# allDataTypes = ['data/glass/glass.json']
	allDataTypes = ['data/wine/wine.json']
	# allDataTypes = ['data/zoo/zoo.json']
	# allDataTypes = ['data/heart/heart.json']
	# allDataTypes = ['data/car/car.json']
	# allDataTypes = ['data/yeast/yeast.json']
	# allDataTypes = ['data/block/pageblocks.json']
	# allDataTypes = ['data/ionosphere/ionosphere.json']

	# allDataTypes = ['data/pendigits/pendigits.json']
	# allDataTypes = ['filenames[5] = "../../data/flare/flare.json']
	# allDataTypes = ['data/letter/letter-recognition.json']

	runsPerDataSet = 1 #10
	for dataSet in allDataTypes:
		setName = dataSet.split('.')[0].split('/')[-1]
		print(setName)
		pSet = PatternSet(dataSet)
		for pat in pSet.patterns:
			pat['h'] = []


		motionDelta = 1.0
		manualStop = False
		iterations = 0
		particleNumber = 2
		minMotionDelta = float(particleNumber*len(pSet.patterns[0]['p']))/10000

		startTime = time.time()
		swarm = Swarm(particleNumber, pSet.patterns)
		while motionDelta > minMotionDelta and not manualStop:
		# for i in range(1000):
			swarm.update()
			motionDelta = sum(sum(abs(v) for v in p.v) for p in Particle.particles)
			iterations = iterations + 1
			if iterations%100 == 0:
				print(str(iterations) + " : " + str(round(motionDelta, 4)) + "/" + str(minMotionDelta))
			if iterations%1000 == 0:
				val = str(raw_input("Should we Stop (y/n)?  "))
				if val is "y":
					manualStop = True
		# update Velocity

		swarm.setParticlesToPersonBest()
		swarm.updateMembership()

		endTime = time.time()
		print("Run Time: [" + str(round(endTime-startTime, 2)) + " sec]")

		with open('psoPlotter/psoMembers.csv', 'w') as file:
			file.write(	str(len(Particle.particles)) + "," + 
						",".join(str(p.bx[0])+","+str(p.bx[1]) for p in Particle.particles) + "," + 
						str(len(swarm.patterns)) + "," + 
						",".join(str(p['p'][0])+","+str(p['p'][1])+","+str(p['m']) for p in swarm.patterns) + "\n")
		if False:
			with open('psoPlotter/psoMembers.csv', 'a') as file:
				for part in swarm.particles:
					file.write(",".join(str(h[0])+","+str(h[1]) for h in part.hx) + "\n")
				for pat in swarm.patterns:
					file.write(",".join(str(h) for h in pat['h']) + "\n")

        means = []
        deviation = []
        for particle in swarm.particles:
        	if len(particle.members) > 0:
	            means.append(patternsMean(particle.members))
	            deviation.append(patternsStandardDeviation(particle.members, patternsMean(particle.members)))
        print means, deviation
        for i, mean in enumerate(means):
            for m in means[i+1:]:
                print euclidianDistance(mean, m)

	print("Done!")
