package main

import (
	"container/list"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
)

type Pattern struct {
	T int
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

func compareClusters(correct []list.List, clustered []list.List) []int {
	count := make([]int, len(correct))
	for i, l := range correct {
		for e := l.Front(); e != nil; e = e.Next() {
			var vector1 []float64
			switch vec := e.Value.(type) {
			case []float64:
				vector1 = vec
			}
			for j, p := range clustered {
				for u := p.Front(); u != nil; u.Next() {
					var vector2 []float64
					switch vec := e.Value.(type) {
					case []float64:
						vector2 = vec
					}
					if vectorDiff(vector1, vector2) < 0.0001 {
						if i == j {
							count[i]++
						}
					}
				}
			}
		}
	}
	return count
}

func getNumClasses(t []int) int {
	classes := list.New()
	for _, class := range t {
		if classes.Len() == 0 {
			classes.PushFront(class)
		} else {
			for e := classes.Front(); e != nil; e.Next() {
				var num int
				switch n := e.Value.(type) {
				case int:
					num = n
				}
				if num != class {
					classes.PushBack(class)
				}
			}
		}
	}
	return classes.Len()
}

func makeClusters(p [][]float64, t []int) (clusters []list.List) {
	clusters = make([]list.List, getNumClasses(t))
	for i, item := range p {
		clusters[t[i]].PushBack(item)
	}
	return clusters
}

func main() {
	filename := "../data/iris/iris.json"
	data := readJson(filename)
	targets := make([]int, len(data))
	patterns := make([][]float64, len(data))
	for i, item := range data {
		targets[i] = item.T
		patterns[i] = item.P
	}
	//trainIndex := int(float64(len(patterns)) * 0.8)
	//fmt.Println(trainIndex)
	correctClusters := makeClusters(patterns, targets)
	clusters, centers := kmeans(getNumClasses(targets), patterns)
	count := compareClusters(correctClusters, clusters)
	fmt.Println("CENTERS:")
	for j := range centers {
		fmt.Println(centers[j])
	}
	for k := 0; k < len(clusters); k++ {
		fmt.Println("CLUSTER:", k)
		fmt.Printf("There are %d elements in this cluster \n", clusters[k].Len())
		for e := clusters[k].Front(); e != nil; e = e.Next() {
			fmt.Println(e.Value)
		}
	}
	fmt.Println(count)
	fmt.Println("Done")
}
