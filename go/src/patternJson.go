package main

import (
	"container/list"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math"
)

type Pattern struct {
	T float64
	P []float64
}

type PatternSet struct {
	Patterns []Pattern
}

func readJson(filename string) (jsonData []Pattern) {
	file, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	err = json.Unmarshal(file, &jsonData)
	if err != nil {
		log.Fatal(err)
	}
	return
}

func vectorCompare(v1 []float64, v2 []float64) bool {
	var same bool = true
	for i := range v1 {
		if math.Abs(v1[i]-v2[i]) > 0.0001 {
			same = false
			break
		}
	}
	return same
}

func findMean(data [][]float64) (mean []float64) {
	return
}

func compareClusters(correct [][][]float64, clustered [][][]float64) []int {
	var done bool = false
	count := make([]int, len(correct))
	for i := range correct {
		for _, v1 := range correct[i] {
			for k := range clustered {
				for _, v2 := range clustered[k] {
					if vectorCompare(v1, v2) {
						if i == k {
							count[i]++
							done = true
							break
						}
					}
				}
				if done {
					break
				}
			}
		}
	}
	return count
}

func getNumClasses(t []float64) int {
	classes := list.New()
	classes.Init()
	count := 1
	var found bool
	for _, class := range t {
		if classes.Len() == 0 {
			classes.PushFront(class)
		} else {
			found = false
			for e := classes.Front(); e != nil; e = e.Next() {
				var num float64
				switch n := e.Value.(type) {
				case float64:
					num = n
				}
				if num == class {
					found = true
					break
				}
			}
			if !found {
				classes.PushBack(class)
				count++
			}
		}
	}
	//fmt.Println(count)
	return count
}

func makeClusters(p [][]float64, t []float64) (clusters [][][]float64) {
	clusters = make([][][]float64, getNumClasses(t))
	for i := range clusters {
		clusters[i] = make([][]float64, 5)
	}
	for i, item := range p {
		clusters[int(t[i])] = append(clusters[int(t[i])], item)
	}
	return clusters
}

func moveClusters(c [][][]float64) [][][]float64 {
	counts := make([][]int, len(c))
	for i := range counts {
		counts[i] = make([]int, len(c))
	}
	//for iter := 0; iter < len(c); iter++ {
	for i := range c {
		for _, elem := range c[i] {
			counts[i][int(elem[len(elem)-1])]++
		}
	}
	//fmt.Println(counts)
	maxs := make([]int, len(c))
	//class := 0
	for i := range counts {
		max := 0
		class := -1
		for j, count := range counts[i] {
			if count > max {
				max = count
				class = j
			}
		}
		if maxs[class] == 0 {
			maxs[class] = max
		} else if maxs[class] <= max {
			for k, item := range maxs {
				if item == 0 {
					maxs[k] = maxs[class]
					maxs[class] = max
				}
			}
		}
	}
	//fmt.Println(maxs)
	//for i, elem := maxs {
	//	for j := range counts {
	//		for k, item := range counts[j] {
	//			if elem == item {
	//				c[j],
	//			}
	//		}
	//	}
	//}
	//c[class], c[iter] = c[iter], c[class]
	//	break
	//}
	//}
	return c
}

func main() {
	filename := "../data/iris/iris.json"
	data := readJson(filename)
	targets := make([]float64, len(data))
	patterns := make([][]float64, len(data))
	for i, item := range data {
		targets[i] = item.T
		patterns[i] = item.P
		//patterns[i] = append(patterns[i], item.T)
	}
	//fmt.Println(trainIndex)
	clusters, centers := kmeans(getNumClasses(targets), patterns)
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
	net.initNet(len(patterns[0]), getNumClasses(targets))
	for i := 0; i < getNumClasses(targets); i++ {
		net.Net[1].Layer[i].Weights = make([]float64, len(patterns[0]))
		net.Net[1].Layer[i].initWeights(patterns)
		fmt.Println(net.Net[1].Layer[i].Weights)
	}

	//net.initWeights(len(patterns[0]) - 1)
	//net.printNet()
	var lClusters [][][]float64 = make([][][]float64, getNumClasses(targets))
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
