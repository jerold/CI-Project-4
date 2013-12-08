package main

import (
	"fmt"
	//"io"
	//"os"
	"vectorOperations"
)

func main() {
	filenames := make(map[int]string, 10)
	filenames[0] = "../../data/iris/iris.json"
	filenames[1] = "../../data/pendigits/pendigits.json"
	filenames[2] = "../../data/wine/wine.json"
	filenames[3] = "../../data/car/car.json"
	filenames[4] = "../../data/zoo/zoo.json"
	filenames[5] = "../../data/flare/flare.json"
	filenames[6] = "../../data/glass/glass.json"
	filenames[7] = "../../data/heart/heart.json"
	filenames[8] = "../../data/letter/letter-recognition.json"
	filenames[9] = "../../data/seeds/seeds.json"
	for x := 0; x < len(filenames); x++ {
		fmt.Println(filenames[x])
		data := readJson(filenames[x])
		//targets := make([]float64, len(data))
		patterns := make([][]float64, len(data))
		for i, item := range data {
			//targets[i] = item.T
			patterns[i] = item.P
			//patterns[i] = append(patterns[i], item.T)
		}
		//fmt.Println(trainIndex)
		clusters, centers := kmeans(3, patterns)
		fmt.Println(len(clusters))
		for y := 0; y < len(centers); y++ {
			fmt.Println(centers[y][0], centers[y][1])
		}
		fmt.Println("CENTERS:")
		for j := range centers {
			fmt.Println(centers[j])
		}
		kMeansDist := make([]float64, len(clusters))
		count := 0
		for k := 0; k < len(clusters); k++ {
			fmt.Println("CLUSTER:", k)
			fmt.Printf("There are %d elements in this cluster \n", len(clusters[k]))
			fmt.Println("The mean of this cluster is", vectorOperations.FindMean(clusters[k]))
			fmt.Println("The variance of this cluster is", vectorOperations.FindVariance(clusters[k], vectorOperations.FindMean(clusters[k])))
			//fmt.Println(clusters[k])
			for i := k + 1; i < len(clusters); i++ {
				kMeansDist[count] = vectorOperations.CalcDistance(centers[i], centers[k])
				count++
			}
		}
		fmt.Println("The distance between clusters is", kMeansDist)

		//correctClusters := makeClusters(patterns, targets)
		//var swapped bool
		//clusters = moveClusters(clusters)
		//count := compareClusters(correctClusters, clusters)
		//fmt.Println(count)

		//competitive learning call on same data
		net := Network{}
		net.initNet(len(patterns[0]), 3)
		for i := 0; i < 3; i++ {
			net.Net[1].Layer[i].Weights = make([]float64, len(patterns[0]))
			net.Net[1].Layer[i].initWeights(patterns)
			fmt.Println(net.Net[1].Layer[i].Weights)
		}

		//var lClusters [][][]float64 = make([][][]float64, vectorOperations.GetNumClasses(targets))
		var lClusters [][][]float64 = make([][][]float64, 3)
		for i := range lClusters {
			lClusters[i] = make([][]float64, 0)
		}
		for _, p := range patterns {
			result := net.compete(p)
			lClusters[result] = append(lClusters[result], p)
		}
		compLearnDist := make([]float64, len(lClusters))
		count = 0
		for i := range lClusters {
			fmt.Println("CLUSTER", i)
			fmt.Printf("There are %d elements in this cluster \n", len(lClusters[i]))
			fmt.Println("The mean of this cluster is", vectorOperations.FindMean(lClusters[i]))
			fmt.Println("The variance of this cluster is", vectorOperations.FindVariance(lClusters[i], vectorOperations.FindMean(lClusters[i])))
			//fmt.Println(lClusters[i])
			for k := i + 1; k < len(lClusters); k++ {
				compLearnDist[count] = vectorOperations.CalcDistance(vectorOperations.FindMean(lClusters[k]), vectorOperations.FindMean(lClusters[i]))
				count++
			}
		}
		fmt.Println("The distance between clusters is", compLearnDist)
	}
	fmt.Println("Done")
}
