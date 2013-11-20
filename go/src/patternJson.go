package main

import (
	//"encoding/json"
	"fmt"
	"log"
	"os"
)

type Pattern struct {
	target     float64
	attributes float64
}

type PatternSet struct {
	patterns []Pattern
}

func readJson(filename string) (p PatternSet) {
	fileInfo, err := os.Stat(filename)
	if err != nil {
		log.Fatal(err)
	}
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(file)
	fmt.Println(fileInfo.Size())
	size := fileInfo.Size()
	data := make([]byte, int(size))
	_, err = file.Read(data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(data)
	//dec := json.NewDecoder(strings.NewReader(jsonStream))
	//for {
	//	var m Message
	//	if err := dec.Decode(&m); err == io.EOF {
	//		break
	//	} else if err != nil {
	//		log.Fatal(err)
	//	}
	//	fmt.Printf("%s: %s\n", m.Name, m.Text)
	//}
	temp := Pattern{10.0, 5.0}
	p = PatternSet{make([]Pattern, 5)}
	p.patterns[0] = temp
	return
}

func main() {
	filename := "../data/iris/iris.json"
	readJson(filename)
}
