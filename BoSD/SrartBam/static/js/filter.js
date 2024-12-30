listPost = {};
$(document).ready(function () {
    startaps = {};
    PrintPosts();
    FilerReader();
    BtnLoadPosts();
    likesCheck();
    ClickEnterProject();


});

const PrintPosts = () => {

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';

    var data = {};

    data['index_action'] = 1;
    data['filter'] = InfoInput();

    // elements = document.getElementsByClassName('section-top-item');
    // console.log(elements);
    console.log(Object.keys(listPost).length);
    // const elements1 = document.querySelectorAll(".section-top-item"); //Обратите внимание на точку перед именем класса
    console.log(listPost);
    count = Object.keys(listPost).length;
    console.log(Object.keys(listPost).length);
    console.log(listPost.length);
    console.log(listPost);
    data['posts'] = listPost;
    console.log(JSON.stringify(data))

    // Отправка пост запроса на сервер
    fetch('/fil_ps', {
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

            // Если сообщение уже есть, удалить текущее
            if (document.querySelector(".sturtups-load") != null) {
                document.querySelector(".sturtups-load").remove();
            }

            // Если сообщение уже есть, удалить текущее
            if (document.querySelector(".user-wrapper-info") != null) {
                document.querySelector(".user-wrapper-info").remove();
            }

            const header_user = document.querySelector(".user-wrapper");
            console.log(header_user)

            if (data['login'] != '') {

                var user_wrapper = create('<button class="btn btn-profile"><div class="user-wrapper-info"><a href="#">' + data['login'] + '</a><img src="../' + data['icon'] + '" alt="user"></div></button>');

                header_user.prepend(user_wrapper);

            } else if (data['login'] == '') {
                var user_wrapper = create('<div class="user-wrapper-info"><button class="btn btn-authorization">Войти</button></div>');
                header_user.prepend(user_wrapper);
            }

            // Выделение элемента main, для последующей вставки в его начало сообщений
            const main = document.querySelector(".main-section");
            const section_top_wrapper = document.querySelector(".section-startups__wrapper");
            console.log(data)
            if (data['status'] == 200) {

                // Вставка div в начало main
                var CountListPost = Object.keys(listPost).length
                console.log(CountListPost);

                // listPost += startaps;
                // console.log(startaps)
                // console.log(Object.keys(startaps).length)
                // console.log(startaps[1]['name'])
                for (i = 1; i <= Object.keys(data['startups']).length; i++) {
                    counti = i + CountListPost
                    section_top_wrapper.append(create('<div class="section-top-item"><button class="btn-enter btn-enter-' + data['startups'][i]['id'] + '"><h3 class="montserrat-alt">' + data['startups'][i]['name'] + '</h3></button><p class="comfortaa">' + data['startups'][i]['description'] + '</p><div class="top-item__like"><button class="btn-like_ps btn-' + data['startups'][i]['id'] + '"><img src="../static/assets/icons/lile.svg" alt="like"></button><p class="montserrat post-likes-' + data['startups'][i]['id'] + '">' + data['startups'][i]['likes'] + '</p></div>'));
                    console.log(i);
                    listPost[i + CountListPost] = data['startups'][i]['id'];
                    startaps[data['startups'][i]['id']] = data['startups'][i];
                }
                section_top_wrapper.append(create('<button class="sturtups-load">Загрузить еще</button>'));


            } else if (data['status'] == 0) {

                // Вставка полученого от сервера сообщения в созданный div
                mes_cuc.innerHTML = "Ошибка авторизации";

                // Вставка div в начало main
                main.before(mes_cuc);
            }
            // listPost += document.getElementsByClassName('section-top-item');


        });

}

const FilerReader = () => {
    // Добавляем обработчики событий после загрузки страницы
    window.onload = function () {
        const selectElement = document.getElementById('filter');
        const inputElement = document.querySelector('input[type="search"]');

        // Обработчик для списка
        selectElement.addEventListener('change', processInput);

        // Обработчик для инпута, реагируем только на нажатие "Enter"
        inputElement.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Отменяем отправку формы
                processInput(); // Вызываем функцию обработки
            }
        });
    };
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

function likesCheck() {
    // Слушатель кнопки 
    $('body').delegate('.btn-like_ps', 'click', function (e) {
        e.preventDefault();
        var str = e.currentTarget.className.split(' ')
        console.log(str);

        var rout = str[0].split('-');
        rout = "/" + rout[1] + ""
        console.log(rout)
        count = str[1].split('-');
        count = count[1];
        console.log(count)

        var data = {};

        console.log(startaps)

        // console.log(star)
        data['index_action'] = 1;
        data['content'] = startaps[count];

        console.log(data)
        console.log(JSON.stringify(data))


        fetch(rout, {
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

                    countstr = "post-likes-" + count;

                    var post_likes = document.getElementsByClassName(countstr);
                    post_likes[0].innerHTML = data['likes'];



                } else if (data['status'] == 0) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = "Ошибка авторизации";

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
        // rout = "/" + rout[2] + ""
        // console.log(rout)
        // count = str[1].split('-');
        // count = count[1];
        // console.log(count)

        // var data = {};

        // console.log(startaps)

        // console.log(star)
        // data['index_action'] = 1;
        // data['content'] = startaps[count];

        // console.log(data)
        // console.log(JSON.stringify(data))

        window.setTimeout(function () { window.location = "/card=" + rout[2]; }, 0);
        // fetch(rout, {
        //     method: 'POST',
        //     body: JSON.stringify(data),
        //     headers: {
        //         'Content-Type': 'application/json'
        //     }
        // })
        //     .then((response) => response.json())
        //     .then((data) => {
        //         console.log(data);

        //         // Если сообщение уже есть, удалить текущее
        //         if (document.querySelector(".messeg") != null) {
        //             document.querySelector(".messeg").remove();
        //         }

        //         // Выделение элемента main, для последующей вставки в его начало сообщений
        //         const main = document.querySelector(".main-section");

        //         if (data['status'] == 200) {

        //             countstr = "post-likes-" + count;

        //             var post_likes = document.getElementsByClassName(countstr);
        //             post_likes[0].innerHTML = data['likes'];



        //         } else if (data['status'] == 0) {

        //             // Вставка полученого от сервера сообщения в созданный div
        //             mes_cuc.innerHTML = "Ошибка авторизации";

        //             // Вставка div в начало main
        //             main.before(mes_cuc);
        //         }


        //     });

    });

};
