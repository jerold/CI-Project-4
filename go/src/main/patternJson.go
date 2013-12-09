package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
)

//pattern class
type Pattern struct {
	P []float64
}

//the set of data vectors lives here
type PatternSet struct {
	Patterns []Pattern
}

//read in the data from a json file
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
