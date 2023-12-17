package main
import "fmt"
func main() {
    var a int = 0
    fmt.Scan(&a)
    x := make([]float64,a)
    y := make([]float64,a)
    for i := 0;i < a;i++ {
        var el int = 0
        fmt.Scan(&el)
        x[i] = float64(el)
    }
    if a >= 2 {
        for i := 1;i < a-1;i++{
            y[i] = (x[i - 1] + x[i] + x[i + 1]) / 3
        }
    }
    y[0] = x[0]
    y[len(y)-1] = x[len(x)-1]
    for i := 0;i < a;i++ {
        var l float64 = y[i]
        fmt.Print(l," ")
    }
}
