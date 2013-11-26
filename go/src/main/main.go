package main

import (
	"fmt"
	"vectorOperations"
)

func main() {
	filename := "../../data/iris/iris.json"
	data := readJson(filename)
	targets := make([]float64, len(data))
	patterns := make([][]float64, len(data))
	for i, item := range data {
		targets[i] = item.T
		patterns[i] = item.P
		//patterns[i] = append(patterns[i], item.T)
	}
	//fmt.Println(trainIndex)
	clusters, centers := kmeans(vectorOperations.GetNumClasses(targets), patterns)
	fmt.Println("CENTERS:")
	for j := range centers {
		fmt.Println(centers[j])
	}
	for k := 0; k < len(clusters); k++ {
		fmt.Println("CLUSTER:", k)
		fmt.Printf("There are %d elements in this cluster \n", len(clusters[k]))
		fmt.Println(clusters[k])
	}
	//correctClusters := makeClusters(patterns, targets)
	//var swapped bool
	//clusters = moveClusters(clusters)
	//count := compareClusters(correctClusters, clusters)
	//fmt.Println(count)

	//competitive learning call on same data
	net := Network{}
	net.initNet(len(patterns[0]), vectorOperations.GetNumClasses(targets))
	for i := 0; i < vectorOperations.GetNumClasses(targets); i++ {
		net.Net[1].Layer[i].Weights = make([]float64, len(patterns[0]))
		net.Net[1].Layer[i].initWeights(patterns)
		fmt.Println(net.Net[1].Layer[i].Weights)
	}

	var lClusters [][][]float64 = make([][][]float64, vectorOperations.GetNumClasses(targets))
	for i := range lClusters {
		lClusters[i] = make([][]float64, 0)
	}
	for _, p := range patterns {
		result := net.compete(p)
		lClusters[result] = append(lClusters[result], p)
	}
	for i := range lClusters {
		fmt.Println("CLUSTER", i)
		fmt.Printf("There are %d elements in this cluster \n", len(lClusters[i]))
		fmt.Println(lClusters[i])
	}
	fmt.Println("Done")
}
