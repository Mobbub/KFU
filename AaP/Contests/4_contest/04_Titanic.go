package main

import (
  "fmt"
  "os"
  "sort"
  "strconv"
  "strings"
)

type person struct {
  pcclass int
  age     int
  sex     string
  name    string
}

type sortPerson []person

func (a sortPerson) Len() int { return len(a) }
func (a sortPerson) Less(i, j int) bool {
  if a[i].age == a[j].age {
    return a[i].name < a[j].name
  }
  return a[i].age < a[j].age
}
func (a sortPerson) Swap(i, j int) { a[i], a[j] = a[j], a[i] }

func split(a string) person {
  var k int = 0
  var f bool = true
  var f_ bool = false
  var buf string = ""
  var res person
  for _, i := range a {
    if i == ',' {
      if f || f_ {
        if k%12 == 2 {
          if buf == "" {
            res.pcclass = -1
          } else {
            res.pcclass, _ = strconv.Atoi(buf)
          }
        } else if k%12 == 3 {
          res.name = buf
        } else if k%12 == 4 {
          res.sex = buf
        } else if k%112 == 5 {
          if buf == "" {
            res.age = -1
          } else {
            res.age, _ = strconv.Atoi(buf)
          }
        }
        buf = ""
        k += 1
      } else {
        buf += ","
      }

    } else if i == '"' && f {
      f = false
    } else if i == '"' && f_ {
      buf = buf + "\""
      f_ = false
    } else if i == '"' {
      f_ = true
    } else {
      buf += string(i)
    }
  }
  return res
}

func main() {
  fileBytes, _ := os.ReadFile("train.csv")
  fileContent := string(fileBytes)
  lines := strings.Split(fileContent, "\r")
  var pclass int
  var age int
  fmt.Scan(&pclass, &age)
  var names []person
  for _, line := range lines[1:] {
    var bufer_person person = split(line)
    if bufer_person.sex == "" || bufer_person.age == -1 || bufer_person.pcclass == -1 || 
bufer_person.name == "" {
      continue
    }
    if bufer_person.sex == "female" && bufer_person.pcclass == pclass && bufer_person.age > age {
      names = append(names, bufer_person)
    }
  }
  sort.Sort(sortPerson(names))
  for _, name := range names {
    fmt.Println(name.name)
  }
}
