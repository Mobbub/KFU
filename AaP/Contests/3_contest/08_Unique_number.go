package main

import "fmt"

func main() {
 var n int
 fmt.Scanln(&n)
 numbers := make(map[int]int)
 for i := 0; i < n; i++ {
  var num int
  fmt.Scan(&num)
  numbers[num]++
 }
 for num, count := range numbers {
  if count%2 != 0 {
   fmt.Println(num)
   break
  }
 }
}
