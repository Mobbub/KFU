package main
import "fmt"
func main() {
    var a,b,c string 
    fmt.Scanln(&a,&b,&c)
    if a == "Нет" && b == "Нет" && c == "Нет"{
        fmt.Println("Кот")
    } else if a == "Нет" && b == "Нет" && c == "Да"{
        fmt.Println("Жираф")   
    } else if a == "Нет" && b == "Да" && c == "Нет"{
        fmt.Println("Курица") 
    } else if a == "Нет" && b == "Да" && c == "Да"{
        fmt.Println("Страус") 
    } else if a == "Да" && b == "Нет" && c == "Нет"{
        fmt.Println("Дельфин")
    } else if a == "Да" && b == "Нет" && c == "Да"{
        fmt.Println("Плезиозавры") 
    } else if a == "Да" && b == "Да" && c == "Нет"{
        fmt.Println("Пингвин") 
    } else if a == "Да" && b == "Да" && c == "Да"{
        fmt.Println("Утка")
    }
}
