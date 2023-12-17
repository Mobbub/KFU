package main
import "fmt"
func main() {
var a,b,n int
fmt.Scan(&a,&b)
fmt.Print("    |")
for y := 1; y <= b;y++ {
        fmt.Printf("%4d",y)
    }
fmt.Print("\n")
fmt.Print("   ")
fmt.Print("--")
for y := 1; y <= b;y++ {
        fmt.Print("----")
    }
fmt.Print("\n")
for x := 1;x <= a;x++ {
    fmt.Printf("%4d|",x)
    for y := 1; y <= b;y++ {
        n = x * y 
        fmt.Printf("%4d",n)
    }
    fmt.Print("\n")
} 
}
