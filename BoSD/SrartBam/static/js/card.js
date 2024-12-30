// Когда браузером прочтён весь документ
$(document).ready(function () {
    let star = {};

    $(document).ready(function () {

        // Создание нового элемента div для отображения в нём сообщения с сервера
        var mes_cuc = document.createElement('div');
        mes_cuc.className += ' flex cuc-regi messeg';

        var data = {};
        data['index_action'] = 1;

        // Отправка пост запроса на сервер
        fetch('/card_ps', {
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

                    var user_wrapper = create('<button class="btn btn-profile"><div class="user-wrapper"> <div class="user-wrapper-info"><a href="#">' + data['login'] + '</a><img src="../' + data['icon_path'] + '" alt="user"></div></button>');
                    header_user.prepend(user_wrapper);

                } else if (data['login'] == '') {
                    var user_wrapper = create('<button class="btn btn-authorization">Войти</button>');
                    header_user.prepend(user_wrapper);
                }

                // Выделение элемента main, для последующей вставки в его начало сообщений
                const main = document.querySelector(".main-section");
                const section_top_wrapper = document.querySelector(".section-card");
                console.log(data)
                if (data['status'] == 200) {

                    // Вставка div в начало main
                    startaps = data;
                    star = startaps

                    console.log(startaps)
                    section_top_wrapper.append(create('<div class="container"><div class="section-card__wrapper"><h2 class="montserrat-alt">' + startaps['name_project'] + '</h2><p><span>Описание: </span>' + startaps['description'] + '</p><p><span>Контакты: </span>' + startaps['contacts'] + '</p></div></div>'));

                } else if (data['status'] == 0) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = "Ошибка авторизации";

                    // Вставка div в начало main
                    main.before(mes_cuc);
                }


            });


    });

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


});
