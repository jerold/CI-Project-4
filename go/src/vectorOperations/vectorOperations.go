package vectorOperations

import (
	"container/list"
	"math"
)

//euclidean distance between two vectors. they must be the same length or this panics
func CalcDistance(v []float64, c []float64) (dist float64) {
	dist = 0.0 //init distance between two vectors to 0
	//loop thru the elements, subtract them, square them and sum em up
	for i := range v {
		dist += math.Pow((v[i] - c[i]), 2)
	}
	//square root the above sum
	dist = math.Sqrt(dist)
	return
}

//subtract two vectors taking the absolute value so it is positive
func VectorDiff(v []float64, c []float64) (diff float64) {
	diff = 0.0
	for i := range v {
		diff += math.Abs(v[i] - c[i])
	}
	return
}

//function to determine if two vectors are the same
func VectorCompare(v1 []float64, v2 []float64) bool {
	var same bool = true
	for i := range v1 {
		if math.Abs(v1[i]-v2[i]) > 0.0001 {
			same = false
			break
		}
	}
	return same
}

//function to find the mean of the input matrix. returns a vector that is the mean.
func FindMean(data [][]float64) (mean []float64) {
	return
}

func CompareClusters(correct [][][]float64, clustered [][][]float64) []int {
	var done bool = false
	count := make([]int, len(correct))
	for i := range correct {
		for _, v1 := range correct[i] {
			for k := range clustered {
				for _, v2 := range clustered[k] {
					if VectorCompare(v1, v2) {
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

//function to determine the number of classes based on input classifications
func GetNumClasses(t []float64) int {
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
	return count
}

//function to make cluster according to input data
func MakeClusters(p [][]float64, t []float64) (clusters [][][]float64) {
	clusters = make([][][]float64, GetNumClasses(t))
	for i := range clusters {
		clusters[i] = make([][]float64, 5)
	}
	for i, item := range p {
		clusters[int(t[i])] = append(clusters[int(t[i])], item)
	}
	return clusters
}

func MoveClusters(c [][][]float64) [][][]float64 {
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
