package main

import (
	"container/list"
	"fmt"
	"math"
	"math/rand"
)

//vars for the number of data vectors and number of attributes in each vector
var (
	numVecs  int = 100
	numAttrs int = 5
)

func main1() {
	//create random data vectors
	data := make([][]float64, numVecs)
	for i := range data {
		data[i] = make([]float64, numAttrs)
		for j := range data[i] {
			data[i][j] = rand.Float64() + float64(j+1)
		}
	}
	//call kmeans with 2-5 clusters and prints some results
	for i := 2; i <= 5; i++ {
		clusters, centers := kmeans(i, data)
		fmt.Println(i, "clusters")
		fmt.Println("CENTERS:")
		for j := range centers {
			fmt.Println(centers[j])
		}
		for k := 0; k < len(clusters); k++ {
			fmt.Println("CLUSTER:", k)
			fmt.Printf("There are %d elements in this cluster \n", clusters[k].Len())
			for e := clusters[k].Front(); e != nil; e = e.Next() {
				fmt.Println(e)
			}
		}
	}
}

//euclidean distance between two vectors. they must be the same length or this panics
func calcDistance(v []float64, c []float64) (dist float64) {
	dist = 0.0
	for i := range v {
		dist += math.Pow((v[i] - c[i]), 2)
	}
	dist = math.Sqrt(dist)
	return
}

//subtract two vectors taking the absolute value so it is positive
func vectorDiff(v []float64, c []float64) (diff float64) {
	diff = 0.0
	for i := range v {
		diff += math.Abs(v[i] - c[i])
	}
	return
}

//calculate kmeans. k is a parameter as well as the data set to be clustered
//returns the centers and an array with the data vectors in each cluster
func kmeans(numClusters int, matrix [][]float64) (clusters []list.List, centers [][]float64) {
	r := rand.New(rand.NewSource(10000))
	centers = make([][]float64, numClusters)
	//make initial random guess at centers
	for i := range centers {
		centers[i] = make([]float64, numAttrs)
		copy(centers[i], matrix[r.Int31n(int32(len(centers)))])
	}
	var change float64 = 1.0
	//main loop. keep interating until there is almost no change in centers.
	for change > 0.0001 {
		//init some arrays to track rolling sums in clusters and members in each cluster
		change = 0.0
		counts := make([]int, numClusters)
		sums := make([][]float64, numClusters)
		clusters = make([]list.List, numClusters)
		for i := range clusters {
			clusters[i].Init()
		}
		//make a new arrays for this iteration to sum each attribute in each cluster to find the mean
		for i := range sums {
			sums[i] = make([]float64, numAttrs)
		}
		//main clustering logic--loop through each input vector
		for i := 0; i < numVecs; i++ {
			bestFit := -1
			minDist := 10000.0
			//loop through each center and see which center is closer to the current input vector
			//fmt.Printf("distances for the %dth vector\n", i)
			for j := 0; j < numClusters; j++ {
				dist := calcDistance(matrix[i], centers[j])
				//fmt.Printf("distance from center %d is %f\n", j, dist)
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
			clusters[bestFit].PushBack(matrix[i])
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
				//this is really not required unless random vectors are created
			} else {
				index := r.Int31n(int32(len(centers)))
				change += vectorDiff(centers[i], matrix[index])
				copy(centers[i], matrix[index])
			}
		}
	}
	return //all done
}
