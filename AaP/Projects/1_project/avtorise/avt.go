package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type User struct {
	Surname      string `json:"surname"`
	Name         string `json:"name"`
	Surname_next string `json:"surname_next"`
	GitHubID     string `json:"github_id"`
	AccessToken  string `json:"access_token"`
	Position     string `json:"position"`
}

type TeChatID struct {
	ChatID string
}

var users = make(map[int64]*User)

var global struct {
	code       string
	authURL    string
	ChID       string
	data_user  string
	data_user1 string
	data_user2 string
	Feedback   string
	Grupp      string
}

const (
	CLIENT_ID     = "dbaca0c66980b1fe7755"
	CLIENT_SECRET = "62bd2934ae480c80ec66d564e2dab9c44bbbbd1b"
)

type UserData struct {
	Id   int64  `json:"id"`
	Name string `json:"name"`
}

func startserver() { //Сервер
	fmt.Println("Start Server ...")
	http.HandleFunc("/Authorization", handlerTransferLink)
	http.HandleFunc("/oauth", handlerOauth)
	http.HandleFunc("/Surgery", surgery)
	http.ListenAndServe("192.168.253.179:8080", nil)
}

func main() { //Запуск сервера
	startserver()
}

func handlerTransferLink(w http.ResponseWriter, r *http.Request) { //тело и переменна w
	//Метод Query() возвращает значения параметров запроса в виде map[string][]string
	ChatID := r.URL.Query().Get("ChatID")
	Surname := r.URL.Query().Get("Surname")
	Name := r.URL.Query().Get("Name")
	Grupp := r.URL.Query().Get("Grupp")
	Surname_next := r.URL.Query().Get("Surname_next")
	fmt.Print(Surname, "\n")
	fmt.Print(Name, "\n")
	fmt.Print(Surname_next, "\n")
	if ChatID == "" {
		fmt.Print("err1")
	}
	fmt.Print("ChatID:", ChatID, "\n")
	URL := Authorization(ChatID, Surname, Name, Surname_next, Grupp)
	fmt.Print(URL, "\n")
	// заголовок и тип отправки
	w.Header().Add("Content-Type", "text/plain")
	// вывод в поток w
	fmt.Fprint(w, URL)
}
func GenerateToken(users *User) string {
	claims := jwt.MapClaims{
		"surname":      users.Surname,
		"name":         users.Name,
		"surname_next": users.Surname_next,
		"github_id":    users.GitHubID,
		"Grupp":        global.Grupp,
		"access_token": users.AccessToken,
		"position":     users.Position,
		"exp":          time.Now().Add(time.Hour * 24).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	secretKey := ("1234")

	signedToken, _ := token.SignedString([]byte(secretKey))
	return signedToken
}
func Authorization(ChatID, Surname, Name, Surname_next, Grupp string) string {
	fmt.Print("Работает", "\n")
	global.ChID = ChatID
	global.data_user = Surname
	global.data_user1 = Name
	global.data_user2 = Surname_next
	global.Grupp = Grupp
	fmt.Print("ChatID", global.ChID, "\n")
	fmt.Print("Surname", global.data_user, "\n")
	fmt.Print("Name", global.data_user1, "\n")
	authURL := "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID + "&state=" + ChatID
	fmt.Print(authURL)
	return authURL
}
func handlerOauth(w http.ResponseWriter, r *http.Request) {
	code := r.URL.Query().Get("code")
	ChatID := r.URL.Query().Get("state")
	fmt.Print("code:", code, "\n")
	fmt.Print("ChatID:", ChatID, "\n")
	if code != " " {
		fmt.Println("Программа работает")
		global.code = code
		AccessToken := getAccessToken(code)
		fmt.Print("AccessToken:", AccessToken, "\n")
		UserData := getUserData(AccessToken)
		Temp := fmt.Sprint(UserData.Id)
		Fed := Feedback(Temp)
		fmt.Print(Fed)
		fmt.Print("UserData.Id:", fmt.Sprint(UserData.Id), "\n")

		if _, ok := users[UserData.Id]; !ok {
			users[UserData.Id] = &User{
				Surname:      global.data_user,
				Name:         global.data_user1,
				Surname_next: global.data_user2,
				GitHubID:     fmt.Sprint(UserData.Id),
				AccessToken:  AccessToken,
				Position:     "student",
			}
		}
		jwtToken := GenerateToken(users[UserData.Id])
		fmt.Print("JWT:", jwtToken, "\n")
		base := Database(jwtToken)
		fmt.Print(base)
	} else {
		temp := "not"
		La := not(temp)
		fmt.Print(La)
	}
}
func not(temp string) string {
	data := struct {
		ChatID string `json:"ChatID"`
		IDgit  string `json:"IDgit"`
	}{
		ChatID: global.ChID,
		IDgit:  "Not",
	}

	// Кодируем JSON-данные в байтовый массив
	jsonData, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}

	// Создаем HTTP POST-запрос
	req, err := http.NewRequest("POST", "http://192.168.253.167:8000/", bytes.NewBuffer(jsonData))
	if err != nil {
		panic(err)
	}

	// Устанавливаем заголовки запроса
	req.Header.Set("Content-Type", "application/json")

	// Отправляем запрос
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	return ""

}

func getAccessToken(code string) string {
	// Создаём http-клиент с дефолтными настройками
	fmt.Print(code)
	client := http.Client{}
	requestURL := "https://github.com/login/oauth/access_token"

	// Добавляем данные в виде Формы
	form := url.Values{}
	form.Add("client_id", CLIENT_ID)
	form.Add("client_secret", CLIENT_SECRET)
	form.Add("code", code)

	// Готовим и отправляем запрос
	request, _ := http.NewRequest("POST", requestURL, strings.NewReader(form.Encode()))
	request.Header.Set("Accept", "application/json") // просим прислать ответ в формате json
	response, _ := client.Do(request)
	defer response.Body.Close()
	// Достаём данные из тела ответа
	var responsejson struct {
		AccessToken string `json:"access_token"`
	}
	json.NewDecoder(response.Body).Decode(&responsejson)
	fmt.Print(responsejson.AccessToken)
	return responsejson.AccessToken
}

func getUserData(AccessToken string) UserData {
	// Создаём http-клиент с дефолтными настройками
	client := http.Client{}
	requestURL := "https://api.github.com/user"

	// Готовим и отправляем запрос
	request, _ := http.NewRequest("GET", requestURL, nil)
	request.Header.Set("Authorization", "Bearer "+AccessToken)
	response, _ := client.Do(request)
	defer response.Body.Close()

	var data UserData
	json.NewDecoder(response.Body).Decode(&data)
	return data
}

func Database(jwtToken string) string {
	fmt.Print("В базу занесся", "\n")
	client := http.Client{}
	URL := fmt.Sprintf("http://192.168.253.55:8060/database?JWT=%s", jwtToken)
	request, err := http.NewRequest("GET", URL, nil)
	if err != nil {
		fmt.Print("errGet")
	}
	response, err := client.Do(request)
	if err != nil {
		fmt.Print("err_requset")
	}
	fmt.Print("В базу занесся", "\n")
	resBody, err := io.ReadAll(response.Body) // Получаем тело ответа
	if err != nil {
		fmt.Print("err_Body")
	}
	defer response.Body.Close()
	return string(resBody)

}
func Feedback(Temp string) string {
	data := struct {
		ChatID string `json:"ChatID"`
		IDgit  string `json:"IDgit"`
	}{
		ChatID: global.ChID,
		IDgit:  Temp,
	}

	// Кодируем JSON-данные в байтовый массив
	jsonData, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}

	// Создаем HTTP POST-запрос
	req, err := http.NewRequest("POST", "http://192.168.253.167:8000/", bytes.NewBuffer(jsonData))
	if err != nil {
		panic(err)
	}

	// Устанавливаем заголовки запроса
	req.Header.Set("Content-Type", "application/json")

	// Отправляем запрос
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	return ""
}

func examination(ID, Request string) string {
	client := http.Client{}
	URL := fmt.Sprintf("http://192.168.253.55:8060/Examination?IdGit=%s&Action=%s", ID, Request)
	request, err := http.NewRequest("GET", URL, nil)
	if err != nil {
		fmt.Print(err)
	}
	response, err := client.Do(request)
	if err != nil {
		fmt.Print("err_requset")
	}
	Body, err := io.ReadAll(response.Body)
	if err != nil {
		fmt.Print("err_Body")
	}
	defer response.Body.Close()
	return string(Body)
}
func surgery(w http.ResponseWriter, r *http.Request) {
	ID := r.URL.Query().Get("IDgit")
	Request := r.URL.Query().Get("Request")
	Exa := examination(ID, Request)
	fmt.Print(Exa)
	if Request == "Где следуящая пара" { // 1 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на понедельник" { // 2 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на вторник" { // 3 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на среду" { // 4 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на четверг" { // 5 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на пяницу" { // 5 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на сегодня" { // 6 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Расписание на завтра" { // 7 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 1ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 2ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 3ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 4ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 5ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 6ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 7ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString) // 1 подгруппа
	} else if Request == "Оставить коментарий к 1ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 2ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 3ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 4ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 5ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 6ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 7ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 1ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 2ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 3ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 4ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 5ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 6ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 7ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 1ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 2ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 3ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 4ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 5ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 6ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Оставить коментарий к 7ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ231" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ231(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ231(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ232" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ232(1)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где ИВТ232(2)" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Корниенко" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Марянин" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Ахрамович" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Вареник" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Томичева" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Ильина" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Кислицина" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Непомнящий" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Руев" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Шестакова" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Фабрина" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Клименко" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Сагайдак" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Галушко" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Горская" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Чабанов" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Рудницкая" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Где Корнута" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	} else if Request == "Когда экзамен" { // 8 вариант
		var SECRET = "123"
		tokeExpiresAt := time.Now().Add(time.Hour * time.Duration(24))

		// Заполняем данными полезную нагрузку
		payload := jwt.MapClaims{
			"Action":     Request,
			"IDG":        ID,
			"Allowed":    "Да",
			"expires_at": tokeExpiresAt.Unix(),
		}

		// Создаём токен с методом шифрования HS256
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

		// Подписываем токен секретным ключом
		tokenString, err := token.SignedString([]byte(SECRET))

		fmt.Printf("Токен: %v\n", tokenString)
		fmt.Printf("Действителен до: %v\n", tokeExpiresAt)
		fmt.Printf("Ошибка: %v\n", err)
		w.Header().Add("Content-Type", "text/plain")
		fmt.Fprint(w, tokenString)
	}
}