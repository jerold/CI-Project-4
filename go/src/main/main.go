package main

import (
	//"bufio"
	//"bytes"
	"fmt"
	//"io"
	"os"
	"strconv"
	"time"
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
	filename1 := "../../results/results.csv"
	filename2 := "../../results/results.txt"
	f1, err := os.Create(filename1)
	if err != nil {
		fmt.Println(err)
	}
	f2, err := os.Create(filename2)
	if err != nil {
		fmt.Println(err)
	}
	defer f1.Close()
	defer f2.Close()
	startTime := time.Now()
	for numClusters := 2; numClusters < 11; numClusters++ {
		f2.WriteString("NUMBER OF CLUSTERS: " + strconv.FormatInt(int64(numClusters), 8) + "\n")
		for x := 0; x < len(filenames); x++ {
			f1.WriteString(strconv.FormatInt(int64(numClusters), 8) + ",")
			f2.WriteString("CURRENT DATA SET: " + filenames[x][5:] + "\n")
			f2.WriteString("================KMEANS===================" + "\n")
			data := readJson(filenames[x])
			patterns := make([][]float64, len(data))
			for i, item := range data {
				patterns[i] = item.P
			}
			clusters, centers := kmeans(numClusters, patterns)
			printDataToCSVFile(f1, clusters, centers, len(data))
			printDataToFile(f2, clusters, float64(len(data)), centers)

			//competitive learning call on same data
			f2.WriteString("================COMPETITIVE LEARNING===================" + "\n")
			net := Network{}
			net.initNet(len(patterns[0]), numClusters)
			for i := 0; i < numClusters; i++ {
				net.Net[1].Layer[i].Weights = make([]float64, len(patterns[0]))
				net.Net[1].Layer[i].initWeights(patterns)
			}

			//var lClusters [][][]float64 = make([][][]float64, vectorOperations.GetNumClasses(targets))
			var lClusters [][][]float64 = make([][][]float64, numClusters)
			for i := range lClusters {
				lClusters[i] = make([][]float64, 0)
			}
			for _, p := range patterns {
				result := net.compete(p)
				lClusters[result] = append(lClusters[result], p)
			}
			centers = make([][]float64, len(lClusters))
			for i, cluster := range lClusters {
				centers[i] = vectorOperations.FindMean(cluster)
			}
			f1.WriteString(strconv.FormatInt(int64(numClusters), 8) + ",")
			printDataToCSVFile(f1, lClusters, centers, len(data))
			printDataToFile(f2, lClusters, float64(len(data)), centers)
		}
	}
	elapsedTime := time.Since(startTime)
	fmt.Println("Total time", elapsedTime.Seconds())
	n, err := f2.WriteString("Total Time: ")
	if err != nil {
		fmt.Println(n, err)
	}
	n, err = f2.WriteString(strconv.FormatFloat(elapsedTime.Seconds(), 'f', 6, 64))
	if err != nil {
		fmt.Println(n, err)
	}
	fmt.Println("Done")
}

func printDataToFile(f *os.File, c [][][]float64, total float64, centers [][]float64) {
	//kMeansDist := make([]float64, 0)
	for k := 0; k < len(c); k++ {
		f.WriteString("CLUSTER:" + strconv.FormatInt(int64(k), 8) + "\n")
		f.WriteString("There is " + strconv.FormatFloat(float64(len(c[k]))/total, 'f', 2, 64) + " percent of the data in this cluster" + "\n")
		f.WriteString("The mean of this cluster is " + vectorOperations.ToString(vectorOperations.FindMean(c[k])) + "\n")
		f.WriteString("The variance of this cluster is " + vectorOperations.ToString(vectorOperations.FindVariance(c[k], vectorOperations.FindMean(c[k]))) + "\n")
		for i := k + 1; i < len(c); i++ {
			f.WriteString("The distance between this cluster and cluster " + strconv.FormatInt(int64(i), 8) + " is " +
				strconv.FormatFloat(vectorOperations.CalcDistance(centers[i], centers[k]), 'f', 6, 64) + "\n")
		}
	}
}

func printDataToCSVFile(f1 *os.File, clusters [][][]float64, centers [][]float64, total int) {
	for i := 0; i < len(centers); i++ {
		f1.WriteString(strconv.FormatFloat(centers[i][0], 'f', 6, 64) + ",")
		f1.WriteString(strconv.FormatFloat(centers[i][1], 'f', 6, 64) + ",")
	}
	f1.WriteString(strconv.FormatInt(int64(total), 8) + ",")
	for i, cluster := range clusters {
		for _, vector := range cluster {
			f1.WriteString(strconv.FormatFloat(vector[0], 'f', 6, 64) + ",")
			f1.WriteString(strconv.FormatFloat(vector[1], 'f', 6, 64) + ",")
			f1.WriteString(strconv.FormatInt(int64(i), 8) + ",")
		}
	}
	f1.WriteString("\n\n\n")
}
