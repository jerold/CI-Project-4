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
