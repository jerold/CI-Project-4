package main

import (
	"math"
	"math/rand"
	"vectorOperations"
)

//calculate kmeans. k is a parameter as well as the data set to be clustered
//returns the centers and an array with the data vectors in each cluster
func kmeans(numClusters int, matrix [][]float64) (clusters [][][]float64, centers [][]float64) {
	r := rand.New(rand.NewSource(10000))
	centers = make([][]float64, numClusters)
	//make initial random guess at centers
	for i := range centers {
		centers[i] = make([]float64, len(matrix[0]))
		copy(centers[i], matrix[r.Int31n(int32(len(centers)))])
	}
	var change float64 = 1.0
	//main loop. keep interating until there is almost no change in centers.
	for change > 0.0001 {
		//init some arrays to track rolling sums in clusters and members in each cluster
		change = 0.0
		counts := make([]int, numClusters)
		sums := make([][]float64, numClusters)
		clusters = make([][][]float64, numClusters)
		for i := range clusters {
			clusters[i] = make([][]float64, 0)
		}
		//make a new arrays for this iteration to sum each attribute in each cluster to find the mean
		for i := range sums {
			sums[i] = make([]float64, len(matrix[0]))
		}
		//main clustering logic--loop through each input vector
		for i := 0; i < len(matrix); i++ {
			bestFit := -1
			minDist := 10000.0
			//loop through each center and see which center is closer to the current input vector
			for j := 0; j < numClusters; j++ {
				dist := vectorOperations.CalcDistance(matrix[i], centers[j])
				if dist < minDist {
					minDist = dist
					bestFit = j
				}
			}
			//counts how many vectors are in each cluster
			counts[bestFit] += 1
			//add this vector's attributes to the rolling sum
			for k := range sums[0] {
				sums[bestFit][k] += matrix[i][k]
			}
			//append this vector to the appropriate cluster
			clusters[bestFit] = append(clusters[bestFit], matrix[i])
		}
		//update the new centers as the mean of values in each cluster
		for i := range centers {
			if counts[i] != 0 {
				for j := range centers[i] {
					newValue := (sums[i][j] / float64(counts[i]))
					change += math.Abs(centers[i][j] - newValue)
					centers[i][j] = newValue
				}
				//if nothing is in this cluster, grab a new vector randomly
				//this is really not required unless random vectors are created randomly
			} else {
				index := r.Int31n(int32(len(centers)))
				change += vectorOperations.VectorDiff(centers[i], matrix[index])
				copy(centers[i], matrix[index])
			}
		}
	}
	return //all done
}
