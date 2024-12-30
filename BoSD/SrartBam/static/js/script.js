$(document).ready(function () {
    var url = location.href;
    var urlFilename = url.substring(url.lastIndexOf('/') + 1);

    if (urlFilename == 'index.html' || urlFilename == 'autorization.html') {
        document.querySelector(".top").classList.add("active");
        document.querySelector(".midle").classList.add("active");
        document.querySelector(".bottom").classList.add("active");
    }

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';

    var mes_eror = document.createElement('div');
    mes_eror.className += ' flex errors messeg';

    var routs = {
        '/reg': '/authorization',
        '/log': '/main',
    };

    // Слушатель кнопки 
    $('body').delegate('.btn', 'click', function (e) {
        e.preventDefault();
        var str = e.currentTarget.className.split(' ')
        var str2 = "." + str[1] + "";
        console.log(str[1]);
        console.log(1);

        var rout1 = str[1].split('-')
        var rout = "/" + rout1[1] + "";
        window.setTimeout(function () { window.location = rout; }, 1000);

        // if (str[1] == "btn-enter") {
        //     window.setTimeout(function () { window.location = "/authorization"; }, 1000);
        // } else if (str[1] == "btn-reg") {
        //     window.setTimeout(function () { window.location = "/register"; }, 1000);
        // }
    });

    // Слушатель кнопки формы
    $('body').delegate('.form', 'submit', function (e) {
        e.preventDefault();
        var str = e.currentTarget.className.split(' ')
        var str2 = "." + str[1] + "";
        console.log(str2);
        console.log(2);

        request = $(str2).serializeArray();

        console.log(request)
        var data = {};
        for (i = 0; i < request.length; i++) {
            data[request[i].name] = request[i].value;
        }

        var rout1 = str[1].split('-')
        var rout = "/" + rout1[1] + "";

        // if (str[1] == "form-reg") {

        //     request = $(".form-reg").serializeArray();

        //     var data = {};
        //     data[request[0].name] = request[0].value;
        //     data[request[1].name] = request[1].value;

        //     rout = '/reg'

        // }

        // if (str[1] == "form-autho") {
        //     request = $(".form-autho").serializeArray();

        //     var data = {};
        //     data[request[0].name] = request[0].value;
        //     data[request[1].name] = request[1].value;

        //     rout = '/log'
        // }

        console.log(routs)
        console.log(rout);
        console.log(data)
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

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = data['message'];

                    // Вставка div в начало main
                    main.before(mes_cuc);

                    // Перенаправление на страницу 
                    window.setTimeout(function () { window.location = routs[rout]; }, 1000);

                } else if (data['status'] == 0) {

                    // Вставка полученого от сервера сообщения в созданный div
                    mes_cuc.innerHTML = "Ошибка авторизации";

                    // Вставка div в начало main
                    main.before(mes_cuc);
                }


            });
    });
});