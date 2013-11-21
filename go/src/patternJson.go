package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	//"os"
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
	//fmt.Println(file)
	err = json.Unmarshal(file, &jsonData)
	if err != nil {
		log.Fatal(err)
	}
	return
}

func main() {
	filename := "../data/iris/iris.json"
	data := readJson(filename)
	//fmt.Println(data)
	targets := make([]int, len(data))
	patterns := make([][]float64, len(data))
	for i, item := range data {
		targets[i] = item.T
		patterns[i] = item.P
	}
	trainIndex := int(float64(len(patterns)) * 0.8)
	fmt.Println(trainIndex)
	clusters, centers := kmeans(3, patterns[:trainIndex])
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
	fmt.Println("Done")
}
