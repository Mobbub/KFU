$(document).ready(function () {

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';

    var mes_eror = document.createElement('div');
    mes_eror.className += ' flex errors messeg';

    startaps = {};
    PrintPosts();

    form_login();


});

// Обработка отправки формы
const form_login = () => {

    // Когда браузером прочтён весь документ
    $(document).ready(function () {


        // Создание нового элемента div для отображения в нём сообщения с сервера
        var mes_cuc = document.createElement('div');
        mes_cuc.className += ' flex cuc-regi messeg';


        // Тригер нажатия на кнопку формы
        $(".form-startup").on("submit", function (event) {
            console.log(1)
            // Запрет на обновление страницы
            event.preventDefault();

            // Подготовка запроса для отправки на сервер
            request = $(".form-startup").serializeArray();

            var data = {};
            data['index_action'] = 1;
            data = request;

            console.log(data);
            // Отправка пост запроса на сервер
            fetch('/startup_ps', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then((response) => response.json())
                .then((data) => {

                    // Если сообщение уже есть, удалить текущее
                    if (document.querySelector(".messeg") != null) {
                        document.querySelector(".messeg").remove();
                    }

                    // Выделение элемента main, для последующей вставки в его начало сообщений
                    const main = document.querySelector(".main-section");

                    if (data['status'] == 200) {

                        // Вставка полученого от сервера сообщения в созданный div
                        mes_cuc.innerHTML = data['message'];

                        // Вставка div в начало main
                        main.before(mes_cuc);

                        // Перенаправление на страницу загрузки схем
                        window.setTimeout(function () { window.location = "/profile"; }, 10000);

                    } else if (data['status'] == 0) {

                        // Вставка полученого от сервера сообщения в созданный div
                        mes_cuc.innerHTML = data['message'];

                        // Вставка div в начало main
                        main.before(mes_cuc);
                    }


                });

        })
    });

}

const PrintPosts = () => {

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';

    var data = {};

    data['index_action'] = 1;

    // Отправка пост запроса на сервер
    fetch('/profile_ps', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((data) => {

            // Если сообщение уже есть, удалить текущее
            if (document.querySelector(".messeg") != null) {
                document.querySelector(".messeg").remove();
            }


            const header_user = document.querySelector(".header-user");
            console.log(header_user)

            if (data['login'] != '') {

                var user_wrapper = create('<button class="btn btn-profile"><div class="user-wrapper-info"><a href="#">' + data['login'] + '</a><img src="../' + data['icon'] + '" alt="user"></div></button>');

                header_user.prepend(user_wrapper);

            } else if (data['login'] == '') {
                var user_wrapper = create('<div class="user-wrapper-info"><button class="btn btn-authorization">Войти</button></div>');
                header_user.prepend(user_wrapper);
            }


        });



}

// Функция для создания html объекта из строки
function create(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}
