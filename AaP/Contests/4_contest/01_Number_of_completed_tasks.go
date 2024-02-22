package main

import (
 "encoding/json"
 "fmt"
 "io/ioutil"
 "os"
)

type Task struct {
 UserID    int    `json:"user_id"`
 ID        int    `json:"id"`
 Title     string `json:"title"`
 Completed bool   `json:"completed"`
}

type Project struct {
 ProjectID int    `json:"project_id"`
 Tasks     []Task `json:"tasks"`
}

func main() {
 var userID int
 fmt.Scan(&userID)
 file, err := os.Open("data.json")
 if err != nil {
  fmt.Println(err)
  return
 }
 defer file.Close()
 data, err := ioutil.ReadAll(file)
 if err != nil {
  fmt.Println(err)
  return
 }
 var projects []Project
 err = json.Unmarshal(data, &projects)
 if err != nil {
  fmt.Println(err)
  return
 }
 completedTasks := 0
 for _, project := range projects {
  for _, task := range project.Tasks {
   if task.UserID == userID && task.Completed {
    completedTasks++
   }
  }
 }
 fmt.Println(completedTasks)
}
