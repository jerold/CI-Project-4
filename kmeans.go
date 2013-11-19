package main

import (
		"math/rand"
		"fmt"
		"math"
		"container/list"
		)
//vars for the number of data vectors and number of attributes in each vector
var (
	 numVecs int = 100
	 numAttrs int = 5
	)

func main() {
	data := make([][]float64, numVecs)
	for i := range(data) {
		data[i] = make([]float64, numAttrs)
		for j := range(data[i]) {
			data[i][j] = rand.Float64() * 10
		}
	}
	for i := 5; i > 0; i-- {
		clusters, centers := kmeans(i, data)
		fmt.Println(i, "clusters")
		fmt.Println("CENTERS:")
		for j := range centers {
			fmt.Println(centers[j])
		}
		for k := 0; k < i; k++ {
			fmt.Println("CLUSTER:", k)
			for e := clusters[k].Front(); e != nil; e = e.Next() {
				fmt.Println(e)
			}
		}
	}
}

func calcDistance(v []float64, c []float64) (dist float64) {
	dist = 0.0
	for i := range(v){
		dist += (math.Pow(v[i], 2) + math.Pow(c[i], 2))
	}
	dist = math.Sqrt(dist)
	return
}

func kmeans(numClusters int, matrix [][]float64) (clusters []list.List, centers [][]float64) {
	centers = make([][]float64, numClusters)
	//make initial random guess at centers
	for i := range(centers) {
		centers[i] = make([]float64, numAttrs)
		for j := range(centers[i]) {
			centers[i][j] = rand.Float64() * 10
		} 
	}
	var change float64 = 1.0
	minDist := 10000.0
	count := 0
	//main loop. keep interating until there is almost no change in centers.
	for change > 0.0001 {
		//init some arrays to track rolling sums in clusters and members in each cluster
		change = 0.0
		counts := make([]int, numClusters)
		sums := make([][]float64, numClusters)
		clusters = make([]list.List, numClusters)
		//make a new arrays for this iteration to sum each attribute in each cluster to find the mean
		for i := range(sums) {
			sums[i] = make([]float64, numAttrs)
		}
		//main clustering logic--loop through each input vector
		for i := 0; i < numVecs; i++ {
			bestFit := 0
			//loop through each center and see which center is closer to the current input vector
			for j := 0; j < numClusters; j++ {
				dist := calcDistance(matrix[i], centers[j])
				if dist < minDist {
					minDist = dist
					bestFit = j
				}
			}
			//counts how many vectors are in each cluster
			counts[bestFit] += 1
			//add this vector's attributes to the rolling sum
			for k := range(sums[0]) {
				sums[bestFit][k] += matrix[i][k]
			}
			//append this vector to the appropriate cluster
			clusters[bestFit].PushBack(matrix[i])
		}
		//update the new centers as the mean of values in each cluster
		for i := range(centers) {
			for j := range(centers[i]) {
				if counts[i] != 0{
					newValue := (sums[i][j] / float64(counts[i]))
					change += math.Abs(centers[i][j] - newValue)
					centers[i][j] = newValue
				}
			}
		}
		count++
	}
	return
}