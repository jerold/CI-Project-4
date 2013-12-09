package vectorOperations

import (
	"container/list"
	"math"
	"strconv"
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

//function to calculate the variance in a cluster of data
func FindVariance(data [][]float64, mean []float64) (variance []float64) {
	variance = make([]float64, len(mean))
	for _, vector := range data {
		for j, item := range vector {
			variance[j] += math.Pow((item - mean[j]), 2.0)
		}
	}
	for i := range variance {
		variance[i] /= float64(len(data) - 1)
	}
	return
}

//function to find the mean of the input matrix. returns a vector that is the mean.
func FindMean(data [][]float64) (mean []float64) {
	if len(data) == 0 {
		mean = make([]float64, 1)
		return
	}
	mean = make([]float64, len(data[0]))
	for _, vector := range data {
		//var sum float64 = 0.0
		for j, item := range vector {
			mean[j] += item
		}
	}
	for i := range mean {
		mean[i] /= float64(len(data))
	}
	return
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

//return a string version of a vector for file writing...ugh go types can get rediculous!
func ToString(vector []float64) string {
	var s string
	s += "["
	for i, elem := range vector {
		s += strconv.FormatFloat(elem, 'f', 6, 64)
		if i == len(vector)-1 {
			s += "]"
		} else {
			s += ", "
		}
	}
	return s
}
