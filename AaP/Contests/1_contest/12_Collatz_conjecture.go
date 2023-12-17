package main
import "fmt"
func main(){
    var a int
    count := 0 
    fmt.Scan(&a)
    for i := 0;a != 1;i++ {
        if a % 2 == 0 {
            a = a / 2
            count++
        } else {
            a = a * 3 + 1
            count++
        }
    }
    fmt.Print(count)
}
