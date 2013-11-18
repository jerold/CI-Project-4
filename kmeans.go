package main

import (
		"math/rand"
		//"container/list"
		"fmt"
		"math"
		)

var (
	 numVecs int = 100
	 numAttrs int = 5)

func main() {
	// data := list.New()
	// data.Init()
	numCenters := 2
	data := make([][]float64, numVecs)
	for i := range(data) {
		data[i] = make([]float64, numAttrs)
		for j := range(data[i]) {
			data[i][j] = rand.Float64() * 10
		}
	}
	 centers := kmeans(numCenters, data)
	 fmt.Println(centers)
	// for i := 0; i < 100; i++{
	// 	vector := new([5]float64)
	// 	for j := 0; j < 5; j++ {
	// 		vector[j] = data[i][j]
	// 	}
	// 	printVector(vector)
	// }
}

func printVector(v *[]float64) {
	fmt.Println(v)
}

func calcDistance(v []float64, c []float64) (dist float64) {
	dist = 0.0
	for i := range(v){
		dist += (math.Pow(v[i], 2) + math.Pow(c[i], 2))
	}
	dist = math.Sqrt(dist)
	return
}

func subtractVectors(v []float64, c []float64) (change float64) {
	change = 0.0
	for i := range(v){
		change += math.Abs(v[i] - c[i])
	}
	return
}

func kmeans(numClusters int, matrix [][]float64) (centers [][]float64) {
	//var centers [][]float64
	centers = make([][]float64, numClusters)
	//clusters := make([][]int, numClusters)
	sums := make([][]float64, numClusters)
	counts := make([]int, numClusters)
	for i := range(centers) {
		centers[i] = make([]float64, numAttrs)
		sums[i] = make([]float64, numAttrs)
		for j := range(centers[i]) {
			centers[i][j] = rand.Float64() * 10
		} 
	}
	//fmt.Println(centers)
	var change float64 = 1.0
	minDist := 10000.0
	count := 0
	for change > 0.0001 {
		change = 0.0
		for i := 0; i < numVecs; i++ {
			bestFit := 0
			for j := 0; j < numClusters; j++ {
				dist := calcDistance(matrix[i], centers[j])
				if dist < minDist {
					minDist = dist
					//fmt.Println(minDist)
					bestFit = j
				}
			}
			counts[bestFit] += 1
			for k := range(sums[0]) {
				sums[bestFit][k] += matrix[i][k]
			}
		}
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
	fmt.Println(count)
	return
}