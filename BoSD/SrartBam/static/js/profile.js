listPost = {};
$(document).ready(function () {

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';

    var mes_eror = document.createElement('div');
    mes_eror.className += ' flex errors messeg';

    startaps = {};
    PrintPosts();
    RemoveBtn();
    BtnLoadPosts();
    FilerReader();
    ClickEnterProject();


});

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

            // // Если сообщение уже есть, удалить текущее
            // if (document.querySelector(".sturtups-load") != null) {
            //     document.querySelector(".sturtups-load").remove();
            // }

            // // Если сообщение уже есть, удалить текущее
            // if (document.querySelector(".user-wrapper-info") != null) {
            //     document.querySelector(".user-wrapper-info").remove();
            // }

            const header_user = document.querySelector(".header-user");
            console.log(header_user)

            if (data['login'] != '') {

                var user_wrapper = create('<div class="user-wrapper-info"><a href="#">' + data['login'] + '</a><img src="../' + data['icon'] + '" alt="user"></div>');

                header_user.prepend(user_wrapper);

            } else if (data['login'] == '') {
                var user_wrapper = create('<div class="user-wrapper-info"><button class="btn btn-authorization">Войти</button></div>');
                header_user.prepend(user_wrapper);
            }
            console.log(data);

            const imgProf = document.querySelector('.imgProf');
            imgProf.src = data['icon'];
            const description = document.querySelector('.description');
            description.value = data['description_profile'];
            const contacts = document.querySelector('.contacts');
            contacts.value = data['contacts'];

            // Выделение элемента main, для последующей вставки в его начало сообщений
            const main = document.querySelector(".main-section");
            const section_top_wrapper = document.querySelector(".user_menu__list");
            console.log(data)
            if (data['status'] == 200) {

                // Вставка div в начало main
                var CountListPost = Object.keys(listPost).length
                console.log(CountListPost);

                for (i = 1; i <= Object.keys(data['startups']).length; i++) {
                    counti = i + CountListPost
                    section_top_wrapper.append(create('<div class="section-top-item section-top-item-' + data['startups'][i]['id'] + '"><button class="btn-enter btn-enter-' + data['startups'][i]['id'] + '"><h3 class="montserrat-alt">' + data['startups'][i]['name'] + '</h3></button><p class="comfortaa">' + data['startups'][i]['description'] + '</p><div class="top-item__like"><button class="btn-like_ps btn-' + data['startups'][i]['id'] + '"><img src="../static/assets/icons/lile.svg" alt="like"></button><p class="montserrat post-likes-' + data['startups'][i]['id'] + '">' + data['startups'][i]['likes'] + '</p></div><button class="btn-remove btn-' + data['startups'][i]['id'] + '"><img src="../static/assets/icons/trashbox.svg" alt="remove"></button>'));
                    console.log(i);
                    listPost[i + CountListPost] = data['startups'][i]['id'];
                    startaps[data['startups'][i]['id']] = data['startups'][i];
                }
                const a = document.querySelector("div.section-top-item::after");
                console.log(a)


            } else if (data['status'] == 0) {

                // // Вставка полученого от сервера сообщения в созданный div
                // mes_cuc.innerHTML = data['status'];

                // // Вставка div в начало main
                // main.before(mes_cuc);
            }
            // listPost += document.getElementsByClassName('section-top-item');


        });

}

const FilerReader = () => {
    // Слушатель кнопки формы
    $('body').delegate('.form-prof', 'submit', function (e) {
        e.preventDefault();


        request = $(".form-prof").serializeArray();

        console.log(request)
        var data = {};
        data['index_action'] = 2;
        data['description_profile'] = request[0].value;
        data['contacts'] = request[1].value;

        console.log(data)
        fetch('/profile_ps', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);

                // Если сообщение уже есть, удалить текущее
                if (document.querySelector(".messeg") != null) {
                    document.querySelector(".messeg").remove();
                }

                // Выделение элемента main, для последующей вставки в его начало сообщений
                const main = document.querySelector(".main-section");
                // Создание нового элемента div для отображения в нём сообщения с сервера
                var mes_cuc = document.createElement('div');
                mes_cuc.className += ' flex cuc-regi messeg';

                var mes_eror = document.createElement('div');
                mes_eror.className += ' flex errors messeg';

                if (data['status'] == 200) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = data['message'];

                    // Вставка div в начало main
                    main.before(mes_cuc);


                } else if (data['status'] == 0) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = data['message'];

                    // Вставка div в начало main
                    main.before(mes_cuc);
                }


            });
        // Готовим файл к отправки на сервер
        const formData = new FormData();
        const files = document.getElementById("file");
        formData.append("file", files.files[0]);

        // Создание параметров запроса
        const requestOptions = {

            mode: "no-cors",
            method: "POST",
            files: files.files[0],
            body: formData,
        };

        // Отправление первого пост запроса на сервер для сохранение файла
        fetch("/icon_ps", requestOptions)
            .then((response) => response.json())
            .then((response) => {

                // Если сообщение уже есть, удалить текущее
                if (document.querySelector(".messeg") != null) {
                    document.querySelector(".messeg").remove();
                }

                const main = document.querySelector(".main-section");

                // Создание нового элемента div для отображения в нём сообщения с сервера
                var mes_cuc = document.createElement('div');
                mes_cuc.className += ' flex cuc-regi messeg';

                var mes_eror = document.createElement('div');
                mes_eror.className += ' flex errors messeg';

                // Проверка что ответ корректный, иначе вывод сообщение об ошибке и выход из addEventListener
                if (response['status'] != 200) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_eror.innerHTML = response['message'];

                    // Вставка div в начало main
                    main.prepend(mes_eror);

                }

            });
    });
}

function InfoInput() {
    // Получаем выбранное значение из списка
    const selectElement = document.getElementById('filter');
    const selectedValue = selectElement.value;

    // Получаем текст из инпута
    const inputElement = document.querySelector('input[type="search"]');
    const inputValue = inputElement.value;

    // Выводим или обрабатываем значения
    console.log('Выбранное значение:', selectedValue);
    console.log('Текст в инпуте:', inputValue);

    filter = {
        'selected': selectedValue,
        'input': inputValue
    }
    return filter

    // Здесь можно добавить логику для обработки этих значений
}

function processInput() {
    // Получаем все элементы с классом 'outer-class'
    const elements = document.querySelectorAll('.section-top-item');

    // Перебираем найденные элементы и удаляем каждый из них
    elements.forEach(element => {
        element.remove();
    });
    listPost = {};
    startaps = {};
    PrintPosts();
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

function BtnLoadPosts() {
    // Слушатель кнопки 
    $('body').delegate('.sturtups-load', 'click', function (e) {
        e.preventDefault();

        PrintPosts();

    });
}

function RemoveBtn() {
    // Слушатель кнопки 
    $('body').delegate('.btn-remove', 'click', function (e) {
        e.preventDefault();
        var str = e.currentTarget.className.split(' ')
        console.log(str);

        var rout = str[1].split('-');


        var data = {};

        console.log(startaps)

        // console.log(star)
        data['index_action'] = 3;
        data['id_proj'] = rout[1];

        console.log(data)
        console.log(JSON.stringify(data))


        fetch('/profile_ps', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);

                // Если сообщение уже есть, удалить текущее
                if (document.querySelector(".messeg") != null) {
                    document.querySelector(".messeg").remove();
                }

                // Выделение элемента main, для последующей вставки в его начало сообщений
                const main = document.querySelector(".main-section");

                if (data['status'] == 200) {

                    const imgProf = document.querySelector('.section-top-item-' + data['id']);
                    imgProf.remove();

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = data['message'];

                    // Вставка div в начало main
                    main.before(mes_cuc);



                } else if (data['status'] == 0) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = data['message'];

                    // Вставка div в начало main
                    main.before(mes_cuc);
                }


            });

    });

};



function ClickEnterProject() {
    // Слушатель кнопки 
    $('body').delegate('.btn-enter', 'click', function (e) {
        e.preventDefault();
        var str = e.currentTarget.className.split(' ')
        console.log(str);

        var rout = str[1].split('-');

        window.setTimeout(function () { window.location = "/card=" + rout[2]; }, 0);

    });

};
