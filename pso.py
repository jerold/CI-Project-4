from patternSet import PatternSet
import time
import random
import math




#--------- Assistance Methods ----------------------------------------------------------
#---------------------------------------------------------------------------------------

def euclidianCopy(p):
	"""Create an copy of the input vector"""
	c = []
	for i in p:
		c.append(i)
	return c

def emptyCopy(p):
	"""Create an empty Vector of the same dimensionality as that of the input vector"""
	c = []
	for i in p:
		c.append(0.0)
	return c

def patternsMean(patterns):
	"""Find the Average value of each element across all of the input patterns assembling and returning a mean pattern"""
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
	"""Standard Deviation vector of the same dimensionality as the patterns and their mean"""
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




#--------- Partical --------------------------------------------------------------------
#---------------------------------------------------------------------------------------

class Particle:
	"""Particles move around the N-Dimensional solution space looking for improved positioning based on certain fitness criteria"""
	particles = []

	def __init__(self, position):
		self.v = self.initVelocity(position)	# Velocity
		self.x = euclidianCopy(position)		# Position
		self.hx = []							# Position History
		self.fitness = 9999.9					# Fitness
		self.fitnessComponents = []
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
		"""Called between iterations to see which patterns are closes to the particle, those become members"""
		self.members = []
		self.memberDistances = []

	def initVelocity(self, position):
		"""Randomly init the velocity of the particle with a value of +OR- 1/3"""
		v = []
		for i, _ in enumerate(position):
			v.append(float(random.randrange(-1000, 1000))/3000)
		return v

	def updateFitness(self):
		"""Calculate the fitness of the particle's current position, updating Personal and Global bests when appropreate"""
		# minimize inter cluster distance
		if len(self.memberDistances) > 0:
			fitnessComponents = []

			avgDist = sum(self.memberDistances)/len(self.memberDistances)
			self.fitness = avgDist									# Reward for being closer to members
			# print("MD:"+str(self.fitness))
			# self.fitness = self.fitness + max(self.memberDistances)
			fitnessComponents.append(avgDist)

			mean = patternsMean(self.members)
			distFromMean = euclidianDistance(self.x, mean)*2
			self.fitness = self.fitness + distFromMean				# Reward for centering on cluster
			# self.fitness = distFromMean
			# print("ED:"+str(self.fitness))
			fitnessComponents.append(distFromMean)

			sd = patternsStandardDeviation(self.members, mean)
			self.fitness = self.fitness + sum(sd)						# Reward for cluster tightness
			# self.fitness = sum(sd)
			# print("SD:"+str(self.fitness))
			fitnessComponents.append(sum(sd))

			if self.fitness < self.bFitness:
				# self.fitnessComponents = fitnessComponents
				# print(allClear)
				self.bx = euclidianCopy(self.x)
				# if self.pIndex == 0:
					# print("B:"+str(self.bFitness)+", F:"+str(self.fitness)+", C:"+str(fitnessComponents))
				self.bFitness = self.fitness
				if self.bFitness < Particle.best.bFitness:
					# print(allClear)
					Particle.best = self
					# for p2 in Particle.particles:
					# 	if p2.pIndex != self.pIndex:
					# 		p2.bFitness = 9999.9
				self.iterationsSinceBestUpdate = 0
			else:
				self.iterationsSinceBestUpdate = self.iterationsSinceBestUpdate + 1
		else:
			self.fitness = 9999.9


	def updatePosition(self):
		"""Update Velocity and then Position"""
		self.updateV()
		self.updateX()

	def updateV(self):
		"""The Velocity Delta is a combination of weighted global bests, personal best, and current velocity values, along with a small random element"""
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
		"""Apply the Velocity Delta to produce the next iteration's position"""
		# Basic position update
		for i, x in enumerate(self.x):
			self.x[i] = x + self.v[i]
		self.hx.append(euclidianCopy(self.x))

		# Effectively turns PSO into K-Means
		# mPat = patternsMean(self.members)
		# for i, v in enumerate(self.x):
		# 	self.x[i] = mPat[i]

	def neighborhoodBest(self):
		"""Neighborhood Best is found from the particle's Star Social Networking, returns the Neighborhood Best's position"""
		neighborCount = 2
		best = Particle.particles[0]
		for particle in Particle.particles[self.pIndex:(self.pIndex+neighborCount)%len(Particle.particles)]:
			if particle.bFitness < best:
				best = particle
		return best.bx

	def globalBest(self):
		"""Returns the Global Best's position"""
		return Particle.best.bx

	def __str__(self):
		"""Sometimes these particles moonlight as strings.  We don't judge"""
		s = "P[" + ", ".join(str(x) + ":" + str(round(self.v[i], 3)) for i, x in enumerate(self.x)) + "]"
		return s




#--------- Swarm Kernal ----------------------------------------------------------------
#---------------------------------------------------------------------------------------

class Swarm:
	"""Swarm Kernal manages iterations and initialization"""
	minV = []
	maxV = []

	def __init__(self, particleCount, patterns):
		Particle.particles = []
		self.patterns = []
		for p in patterns:
			self.patterns.append(p)
		self.particles = self.initParticles(particleCount, patterns)

	def initParticles(self, particleCount, patterns):
		"""The initial particle population is produced within the input space (min-max for each dimension of the patterns"""
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
		"""Range is found in the initParticles method and is used here to produce a random position in the solution space"""
		newPattern = emptyCopy(self.patterns[0]['p'])
		for i, _ in enumerate(newPattern):
			try:
				newPattern[i] = float(random.randrange(int(Swarm.minV[i]*1000), int(Swarm.maxV[i]*1000)))/1000
			except ValueError:
				newPattern[i] = 0.0
		return newPattern

	def update(self):
		"""Kernal handles the iteration work"""
		self.checkProximity()
		self.updateMembership()
		self.updateParticles()

	def checkProximity(self):
		"""To prevent particles from getting ontop of eachother, the Swarm teleports them to random locations if the get too friendly"""
		for p1 in self.particles:
			for p2 in self.particles:
				if p1.pIndex != p2.pIndex and euclidianDistance(p1.bx, p2.bx) < 0.5:
					print("Get out of Here <-------------<<<")
					p1.bFitness = 9999.9
					p1.initVelocity(self.randomPositionInRange())

	def updateMembership(self):
		"""Membership is determined strictly on proximity.  The patterns become 'members' of the nearest particle"""
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
		"""Particles first have their fitness evaluated so Neighborhood and Global Bests are up to date when velocity is calculated"""
		for particle in self.particles:
			particle.updateFitness()
		for particle in self.particles:
			particle.updatePosition()

	def setParticlesToPersonBest(self):
		"""At the end of each run, the particles are returned to their Personal Best position for which final membership is then determined"""
		for particle in self.particles:
			for i, x in enumerate(particle.x):
				particle.v[i] = particle.x[i] - particle.bx[i]
			particle.updateX()




#--------- Main Method -----------------------------------------------------------------
#---------------------------------------------------------------------------------------

if __name__=="__main__":
	# Batch: (ordered by least time complex to most)
	allDataTypes = ['data/iris/iris.json',
					 'data/seeds/seeds.json',
					 'data/glass/glass.json',
					 'data/wine/wine.json',
					 'data/zoo/zoo.json',
					 'data/heart/heart.json',
					 'data/car/car.json',
					 'data/yeast/yeast.json',
					 'data/block/pageblocks.json',
					 'data/ionosphere/ionosphere.json',
					 'data/pendigits/pendigits.json',
					 'data/flare/flare.json',
					 'data/letter/letter-recognition.json']

	# Single:
	# allDataTypes = ['psoTestSet.json']
	# allDataTypes = ['data/iris/iris.json']
	# allDataTypes = ['data/seeds/seeds.json']
	# allDataTypes = ['data/glass/glass.json']
	# allDataTypes = ['data/wine/wine.json']
	# allDataTypes = ['data/zoo/zoo.json']
	# allDataTypes = ['data/heart/heart.json']
	# allDataTypes = ['data/car/car.json']
	# allDataTypes = ['data/yeast/yeast.json']
	# allDataTypes = ['data/block/pageblocks.json']
	# allDataTypes = ['data/ionosphere/ionosphere.json']

	# allDataTypes = ['data/pendigits/pendigits.json']
	# allDataTypes = ['data/flare/flare.json']
	# allDataTypes = ['data/letter/letter-recognition.json']

	runsPerDataSet = 1 #10
	kRange = range(2, 10)
	for k in kRange:
		for dataSet in allDataTypes:
			setName = dataSet.split('.')[0].split('/')[-1]
			print(setName)
			pSet = PatternSet(dataSet)
			for pat in pSet.patterns:
				pat['h'] = []


			motionDelta = 1.0
			manualStop = False
			iterations = 0
			particleNumber = k
			minMotionDelta = float(particleNumber*len(pSet.patterns[0]['p']))/10000

			startTime = time.time()
			swarm = Swarm(particleNumber, pSet.patterns)
			for i in range(5000):
				swarm.update()
				motionDelta = sum(sum(abs(v) for v in p.v) for p in Particle.particles)
				iterations = iterations + 1
				# if iterations%500 == 0:
				# 	print(str(iterations) + " : " + str(round(motionDelta, 4)) + "/" + str(minMotionDelta))

			swarm.setParticlesToPersonBest()
			swarm.updateMembership()

			endTime = time.time()
			print("Run Time: [" + str(round(endTime-startTime, 2)) + " sec]")

			with open('records/psoResults.txt', 'a') as file:
				file.write('\n\nNUMBER OF CLUSTERS: ' + str(particleNumber) + '\n')
				file.write('CURRENT DATA SET: ' + str(setName) + '\n')
				file.write('================PARTICLE SWARM================\n')
				for i, p1 in enumerate(Particle.particles):
					file.write('CLUSTER:' + str(p1.pIndex) + '\n')
					file.write('Cluster contains ' + str(float(len(p1.members))/len(pSet.patterns)) + ' percent of the data\n')
					mean = patternsMean(p1.members)
					file.write('Cluster mean is ' + str(mean) + '\n')
					file.write('Cluster standard deviation is ' + str(patternsStandardDeviation(p1.members, mean)) + '\n')
					for j, p2 in enumerate(Particle.particles):
						if j > i:
							file.write('The distance between this cluster and cluster ' + str(p2.pIndex) + ' is ' + str(euclidianDistance(p1.x, p2.x)) + '\n')

			with open('psoPlotter/psoMembers.csv', 'w') as file:
				file.write(	str(len(Particle.particles)) + "," + 
							",".join(str(p.bx[0])+","+str(p.bx[1]) for p in Particle.particles) + "," + 
							str(len(swarm.patterns)) + "," + 
							",".join(str(p['p'][0])+","+str(p['p'][1])+","+str(p['m']) for p in swarm.patterns) + "\n")
			if True:
				with open('psoPlotter/psoMembers.csv', 'a') as file:
					for part in swarm.particles:
						file.write(",".join(str(h[0])+","+str(h[1]) for h in part.hx) + "\n")
					for pat in swarm.patterns:
						file.write(",".join(str(h) for h in pat['h']) + "\n")

	        # means = []
	        # deviation = []
	        # for particle in swarm.particles:
	        # 	if len(particle.members) > 0:
		       #      means.append(patternsMean(particle.members))
		       #      deviation.append(patternsStandardDeviation(particle.members, patternsMean(particle.members)))
	        # print means, deviation
	        # for i, mean in enumerate(means):
	        #     for m in means[i+1:]:
	        #         print euclidianDistance(mean, m)

	print("Done!")
