package main

import (
	"context"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/dgrijalva/jwt-go"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type User struct {
	Surname      string `bson:"surname"`
	Name         string `bson:"name"`
	Surname_next string `bson:"surname_next"`
	Github_id    string `bson:"github_id"`
	Grupp        string `bson:"groupe"`
	Access_token string `bson:"access_token"`
	Position     string `bson:"position"`
	Exp          string `bson:"exp"`
}

type Schedule struct {
	ID          string `bson:"_id"`
	SchID       string `bson:"SchID"`
	FirstPair   Pair   `bson:"первая пара"`
	SecondPair  Pair   `bson:"вторая пара"`
	ThirdPair   Pair   `bson:"третья пара"`
	FourthPair  Pair   `bson:"четвертая пара"`
	FifthPair   Pair   `bson:"пятая пара"`
	SixthPair   Pair   `bson:"шестая пара"`
	SeventhPair Pair   `bson:"седьмая пара"`
}

type Pair struct {
	Subject   string `bson:"предмет"`
	PairType  string `bson:"тип пары"`
	Classroom string `bson:"аудитория"`
	Lecturer  string `bson:"лектор"`
	Message   string `bson:"сообщение"`
}

var Skey = []byte("1234")

func jwtcheck(tokenstr string) (*jwt.MapClaims, error) { //принимать JWT
	var parsedToken *jwt.Token
	JWTtokeninfo := jwt.MapClaims{}

	parsedToken, err := jwt.ParseWithClaims(tokenstr, &JWTtokeninfo, func(token *jwt.Token) (interface{}, error) { // парсинг токена

		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok { // проверяет подпись
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}

		return Skey, nil

	})

	if err != nil {
		fmt.Println(err)
		return nil, err
	}

	if !parsedToken.Valid {
		fmt.Println("Неверный токен")
		return nil, fmt.Errorf("Неверный токен")
	}

	return &JWTtokeninfo, nil
}

func ConnectMongoDB() (*mongo.Database, error) {
	clientOptions := options.Client().ApplyURI("mongodb+srv://Aboba:1van@ivan.vi217jg.mongodb.net/?retryWrites=true&w=majority")

	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		return nil, err
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		return nil, err
	}

	sched := client.Database("schedule")
	return sched, nil

}

func main() {

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { // обработчик
		path := r.URL.Path // извлечение пути
		if path == "/protected" {
			tokenstr := r.Header.Get("Authorization") // извлечение токена из заголовка Authorization
			// Удалить префикс 'Bearer '
			tokenstr = strings.TrimPrefix(tokenstr, "Bearer ")

			token, err := jwtcheck(tokenstr) // проверка на валидность
			if err != nil {
				w.WriteHeader(http.StatusUnauthorized)
				return
			}

			claims := *token // значения токена

			w.Write([]byte("токен получен"))
			githubID, _ := strconv.Atoi(claims["github_id"].(string)) //преобразование

			db, _ := ConnectMongoDB()

			_ = checkAndAddUser(db, githubID, claims)

			fmt.Println("Token is valid")
			return
		}
		if path == "/Examination" { //проверка пути
			handlerYesNo(w, r)
			return
		}
		if path == "/upload" {
			uploadFile(w, r)
			return
		}
		if path == "/tgbot" {
			tokenString := r.Header.Get("Authorization")
			handleCustomJWT(tokenString)
		}
	})

	http.ListenAndServe(":8060", nil)

}

func handlerYesNo(w http.ResponseWriter, r *http.Request) {
	github_id := r.URL.Query().Get("idGit")
	Action := r.URL.Query().Get("Action")

	db, err := ConnectMongoDB()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	user, err := findUserByID(db, github_id) //поиск пользователя
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	allowed := isActionAllowed(user.Position, Action) //проверка разрешения
	if allowed {
		fmt.Fprintf(w, "Да")
	} else {
		fmt.Fprintf(w, "Нет")
	}
}

func findUserByID(db *mongo.Database, github_id string) (User, error) { //поиск пользователя
	var user User

	collection := db.Collection("users")
	filter := bson.M{"github_id": github_id}

	err := collection.FindOne(context.Background(), filter).Decode(&user)
	if err != nil {
		return User{}, err
	}

	return user, nil
}

func isActionAllowed(position string, action string) bool {
	if position == "преподаватель" {
		switch action {
		case "Где следующая пара", "Расписание на понедельник", "Расписание на вторник", "Расписание на среду", "Расписание на четверг", "Расписание на пятницу", "Расписание на сегодня", "Расписание на завтра", "Оставить комментарий к [номер] паре [для группы]", "Где группа / подгруппа":
			return true
		}
	} else if position == "студент" {
		switch action {
		case "Где следующая пара", "Расписание на понедельник", "Расписание на вторник", "Расписание на среду", "Расписание на четверг", "Расписание на пятницу", "Расписание на сегодня", "Расписание на завтра", "Где преподаватель", "Когда экзамен":
			return true
		}
	}

	return false
}

func checkAndAddUser(db *mongo.Database, githubID int, claims jwt.MapClaims) error {

	usersCollection := db.Collection("users")

	filter := bson.M{"github_id": strconv.Itoa(githubID)}
	var user User

	err := usersCollection.FindOne(context.TODO(), filter).Decode(&user) //поиск пользователя

	if err != mongo.ErrNoDocuments {
		return nil
	}

	user = User{
		Github_id:    strconv.Itoa(githubID),
		Surname:      claims["surname"].(string),
		Name:         claims["name"].(string),
		Surname_next: claims["surname_next"].(string),
		Access_token: claims["access_token"].(string),
		Position:     claims["position"].(string),
		Grupp:        claims["groupe"].(string),
		Exp:          claims["exp"].(string),
	}

	_, err = usersCollection.InsertOne(context.TODO(), user)

	return err
}

func handleCustomJWT(tokenString string) { // принимает jwt токен от тг бота

	token, err := jwtcheckCustom(tokenString) // проверка токена от бота
	if err != nil {
		return
	}

	claims := *token

	action := claims["Action"].(string) // извлечение из полей токена
	githubID := claims["IDG"].(string)

	db, err := ConnectMongoDB()
	if err != nil {
		return
	}

	user, err := findUserByID(db, githubID) // поиск по id
	if err != nil {
		return
	}

	group := user.Grupp

	now := time.Now()     //текущее время
	day, _ := getDay(now) // получение текущего для

	switch action {

	case "Где следующая пара":
		pairNum := getCurrentPairNumber(now)
		schID := assembleScheduleID(group, day)
		schedule, err := findScheduleByID(db, schID)
		if err != nil {
			return
		}
		fmt.Println(getNextPairInfo(schedule, pairNum))

	case "Расписание на понедельник":
		schID := assembleScheduleID(group, "понедельник")
		schedule, err := findScheduleByID(db, schID)
		if err != nil {
			return
		}
		fmt.Println(getScheduleInfo(schedule))

	case "Оставить комментарий к [номер] паре [для группы]":
		pairNum, group := parsePairComment(action)
		schID := assembleScheduleID(group, day)
		schedule, err := findScheduleByID(db, schID)
		if err != nil {
			return
		}
		updatePairComment(db, schedule, pairNum, "Новый комментарий")

	case "Где группа / подгруппа":
		pairNum := getCurrentPairNumber(now)
		schID := assembleScheduleID(group, day)
		schedule, err := findScheduleByID(db, schID)
		if err != nil {
			return
		}
		fmt.Println(getPairInfo(schedule, pairNum))

	case "Где преподаватель":
		pairNum := getCurrentPairNumber(now)
		schID := assembleScheduleID(group, day)
		schedule, err := findScheduleByID(db, schID)
		if err != nil {
			return
		}
		lecturer := getPairLecturer(schedule, pairNum)
		fmt.Println("Преподаватель", lecturer, "в аудитории", getPairClassroom(schedule, pairNum))
		break

	case "Когда экзамен":
		fmt.Println("Экзамен 16.01")
	}

}

func findScheduleByID(db *mongo.Database, schID string) (Schedule, error) { //поиск по id
	var user User

	collection := db.Collection("users")
	filter := bson.M{"github_id": schID}

	err := collection.FindOne(context.Background(), filter).Decode(&user)
	if err != nil {
		return Schedule{}, err
	}

	return Schedule{}, nil
}

func jwtcheckCustom(tokenString string) (*jwt.MapClaims, error) { // парсинг токена

	var parsedToken *jwt.Token
	JWTtokeninfo := jwt.MapClaims{}

	parsedToken, err := jwt.ParseWithClaims(tokenString, &JWTtokeninfo, func(token *jwt.Token) (interface{}, error) {

		return []byte("123"), nil
	})

	if err != nil {
		return nil, err
	}

	if !parsedToken.Valid {
		return nil, errors.New("Invalid token")
	}

	return &JWTtokeninfo, nil

}

func getDay(now time.Time) (string, string) {
	weekday := now.Weekday()
	var day string
	switch weekday {
	case time.Monday:
		day = "понедельник"
	case time.Tuesday:
		day = "вторник"
	case time.Wednesday:
		day = "среда"
	case time.Thursday:
		day = "четверг"
	case time.Friday:
		day = "пятница"
	case time.Saturday:
		day = "суббота"
	case time.Sunday:
		day = "воскресенье"
	}

	return day, "день"
}

func getNextPairInfo(schedule Schedule, pairNum int) string {
	var nextPair Pair

	switch pairNum {
	case 1:
		nextPair = schedule.SecondPair
	case 2:
		nextPair = schedule.ThirdPair
	case 3:
		nextPair = schedule.FourthPair
	case 4:
		nextPair = schedule.FifthPair
	case 5:
		nextPair = schedule.SixthPair
	case 6:
		nextPair = schedule.SeventhPair
	default:
		nextPair = schedule.FirstPair // на случай > 6
	}

	return fmt.Sprintf("%s в %s у %s",
		nextPair.Subject, nextPair.Classroom, nextPair.Lecturer)
}

func updatePairComment(db *mongo.Database, schedule Schedule, pairNum int, comment string) {
	collection := db.Collection("schedules")

	filter := bson.M{"_id": schedule.ID}

	var updateField string
	switch pairNum {
	case 1:
		updateField = "FirstPair.Message"
	case 2:
		updateField = "SecondPair.Message"
	case 3:
		updateField = "ThirdPair.Message"
	case 4:
		updateField = "FourthPair.Message"
	case 5:
		updateField = "FifthPair.Message"
	case 6:
		updateField = "SixthPair.Message"
	case 7:
		updateField = "SeventhPair.Message"
	}

	update := bson.M{
		"$set": bson.M{
			updateField: comment,
		},
	}

	_, err := collection.UpdateOne(
		context.TODO(),
		filter,
		update,
		options.Update().SetUpsert(true),
	)

	if err != nil {
		return
	}
}

func parsePairComment(text string) (int, string) {
	re := regexp.MustCompile(`(\d+) паре (.*)`)
	matches := re.FindStringSubmatch(text)

	pairNum, _ := strconv.Atoi(matches[1])
	group := matches[2]

	return pairNum, group
}

func getCurrentPairNumber(now time.Time) int {
	hour := now.Hour()

	if hour >= 8 && hour < 10 {
		return 1
	} else if hour >= 10 && hour < 11 {
		return 2
	} else if hour >= 11 && hour < 13 {
		return 3
	} else if hour >= 13 && hour < 15 {
		return 4
	} else if hour >= 15 && hour < 17 {
		return 5
	} else if hour >= 17 && hour < 19 {
		return 6
	} else if hour >= 19 && hour < 21 {
		return 7
	}

	return 0
}

func assembleScheduleID(group string, day string) string {

	var week string
	if time.Now().Weekday()%2 == 0 {
		week = "чет"
	} else {
		week = "нечет"
	}

	dayInt, _ := strconv.Atoi(day)

	return group + "-" + week + "-" + strconv.Itoa(dayInt)
}

func getScheduleInfo(schedule Schedule) string {

	info := ""

	info += "Первая пара: " + schedule.FirstPair.Subject + " " +
		schedule.FirstPair.Lecturer + " " + schedule.FirstPair.Classroom

	info += "\nВторая пара: " + schedule.SecondPair.Subject + " " +
		schedule.SecondPair.Lecturer + " " + schedule.SecondPair.Classroom

	info += "\nТретья пара: " + schedule.ThirdPair.Subject + " " +
		schedule.ThirdPair.Lecturer + " " + schedule.ThirdPair.Classroom

	info += "\nЧетвертая пара: " + schedule.FourthPair.Subject + " " +
		schedule.FourthPair.Lecturer + " " + schedule.FourthPair.Classroom

	info += "\nПятая пара: " + schedule.FifthPair.Subject + " " +
		schedule.FifthPair.Lecturer + " " + schedule.FifthPair.Classroom

	info += "\nШестая пара: " + schedule.SixthPair.Subject + " " +
		schedule.SixthPair.Lecturer + " " + schedule.SixthPair.Classroom

	info += "\nСедьмая пара: " + schedule.SeventhPair.Subject + " " +
		schedule.SeventhPair.Lecturer + " " + schedule.SeventhPair.Classroom

	return info
}

func getPairInfo(schedule Schedule, pairNum int) string {

	var pair Pair

	switch pairNum {
	case 1:
		pair = schedule.FirstPair
	case 2:
		pair = schedule.SecondPair
	case 3:
		pair = schedule.ThirdPair
	case 4:
		pair = schedule.FourthPair
	case 5:
		pair = schedule.FifthPair
	case 6:
		pair = schedule.SixthPair
	case 7:
		pair = schedule.SeventhPair
	}

	return pair.Subject + " " + pair.Lecturer + " " + pair.Classroom
}

func getPairLecturer(schedule Schedule, pairNum int) string {

	var pair Pair

	switch pairNum {
	case 1:
		pair = schedule.FirstPair
	case 2:
		pair = schedule.SecondPair
	case 3:
		pair = schedule.ThirdPair
	case 4:
		pair = schedule.FourthPair
	case 5:
		pair = schedule.FifthPair
	case 6:
		pair = schedule.SixthPair
	case 7:
		pair = schedule.SeventhPair
	}

	return pair.Lecturer
}

func getPairClassroom(schedule Schedule, pairNum int) string {

	var pair Pair

	switch pairNum {
	case 1:
		pair = schedule.FirstPair
	case 2:
		pair = schedule.SecondPair
	case 3:
		pair = schedule.ThirdPair
	case 4:
		pair = schedule.FourthPair
	case 5:
		pair = schedule.FifthPair
	case 6:
		pair = schedule.SixthPair
	case 7:
		pair = schedule.SeventhPair
	}

	return pair.Classroom
}

func uploadFile(w http.ResponseWriter, r *http.Request) {
	fmt.Println("File Upload Endpoint Hit")

	r.ParseMultipartForm(10 << 20)

	file, handler, err := r.FormFile("file")
	if err != nil {
		fmt.Println("Error Retrieving the File")
		fmt.Println(err)
		return
	}
	defer file.Close()

	fmt.Printf("Uploaded File: %+v\n", handler.Filename)
	fmt.Printf("File Size: %+v\n", handler.Size)
	fmt.Printf("MIME Header: %+v\n", handler.Header)

	tempFile, err := os.Create("output.json")
	if err != nil {
		fmt.Println(err)
	}
	defer tempFile.Close()

	fileBytes, err := ioutil.ReadAll(file)
	if err != nil {
		fmt.Println(err)
	}

	content := string(fileBytes)

	idx := strings.LastIndex(content, "}]]")
	if idx != -1 {

		content = content[:idx+len("}]]")]
	}

	tempFile.Write([]byte(content))
	fmt.Fprintf(w, "Successfully Uploaded File\n")
}
