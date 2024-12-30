// Когда браузером прочтён весь документ
$(document).ready(function () {
    startaps = {};

    $(document).ready(function () {

        // Создание нового элемента div для отображения в нём сообщения с сервера
        var mes_cuc = document.createElement('div');
        mes_cuc.className += ' flex cuc-regi messeg';

        var data = {};
        data['index_action'] = 1;

        // Отправка пост запроса на сервер
        fetch('/main_ps', {
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
                const section_top_wrapper = document.querySelector(".section-top-wrapper");
                console.log(data)
                if (data['status'] == 200) {

                    // Вставка div в начало main
                    console.log(data['startups'])
                    // startaps = data['startups'];
                    // star = startaps

                    // console.log(startaps)
                    // console.log(Object.keys(startaps).length)
                    // console.log(startaps[1]['name'])
                    for (i = 1; i <= Object.keys(data['startups']).length; i++) {
                        section_top_wrapper.append(create('<div class="section-top-item"><button class="btn-enter btn-enter-' + data['startups'][i]['id'] + '"><h3 class="montserrat-alt">' + data['startups'][i]['name'] + '</h3></button><p class="comfortaa">' + data['startups'][i]['description'] + '<div class="top-item__like"><button class="btn-like_ps btn-' + data['startups'][i]['id'] + '"><img src="../static/assets/icons/lile.svg" alt="like"></button><p class="montserrat post-likes-' + data['startups'][i]['id'] + '">' + data['startups'][i]['likes'] + '</p></div></div>'));
                        startaps[data['startups'][i]['id']] = data['startups'][i];
                    }

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
        console.log(startaps)


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
});