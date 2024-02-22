package main

import (
 "fmt"
 "sort"
)

func twoSum(numbers []int, target int) []int {
    result := make([]int, 2)
    seen := make(map[int]int)
    for i, num := range numbers {
        if j, ok := seen[target-num]; ok {
            result[0] = numbers[j]
            result[1] = num
            return result
        }
        seen[num] = i
    }
    return result
}

func main() {
    var sequenceSize int
    var target int
    fmt.Scan(&sequenceSize, &target)
    numbers := make([]int, sequenceSize)
    for i := 0; i < len(numbers); i++ {
        fmt.Scan(&numbers[i])
    }
    result := twoSum(numbers, target)
    sort.Ints(result)
    for _, number := range result {
        fmt.Print(number, " ")
    }
}
