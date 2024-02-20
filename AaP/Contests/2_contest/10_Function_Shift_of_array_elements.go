import "math"

func shiftArrayRight(data []int, steps int) {
	arrayLength := len(data)
	var absSteps int = int(math.Abs(float64(steps % arrayLength)))
	temp := make([]int, absSteps)
	copy(temp, data[arrayLength-absSteps:])
	copy(data[absSteps:], data[:arrayLength-absSteps])
	copy(data, temp)
}

func shiftArrayLeft(data []int, steps int) {
	arrayLength := len(data)
	var absSteps int = int(math.Abs(float64(steps % arrayLength)))
	temp := make([]int, absSteps)
	copy(temp, data[:absSteps])
	copy(data[:arrayLength-absSteps], data[absSteps:])
	copy(data[arrayLength-absSteps:], temp)
}

func shift(data []int, steps int) {
	if steps > 0 {
		shiftArrayRight(data, steps)
	} else {
		shiftArrayLeft(data, steps)
	}
}
