package main
import "fmt"
func main(){
    var a int
    b := 0
    c := 0
    z := 0 
    h := 0 
    g := 0 
    fmt.Scan(&a)
    if a >= 5000 {
        for b = 0; a >= 5000;b++ {
            a = a - 5000 
        }  
    } 
    if a >= 1000{
        for c = 0; a >= 1000;c++ {
            a = a - 1000
        }
    }
    if a >= 500{
        for z = 0; a >= 500;z++ {
            a = a - 500
        }
        
    }
    if a >= 200{
        for g = 0; a >= 200;g++ {
            a = a - 200
        }
    }
    if a >= 100{
        for h = 0; a >= 100;h++ {
            a = a - 100
        }
    }
    fmt.Print(b,c,z,g,h)
}
