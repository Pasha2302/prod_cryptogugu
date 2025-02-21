'use strict';


var request = (_url, _method, query_data = null) => {
    // Получаем CSRF-токен
    // var csrftoken = getCookie("csrftoken");

    var requestOptions = {
        method: _method,
        headers: {
            "Content-Type": "application/json",
            // "X-CSRFToken": csrftoken,
            "X-CSRFToken": csrf_token,
        },
    };

    if (_method === "POST" || _method === "PUT") {
        var dataToSave = { data: query_data };
        requestOptions.body = JSON.stringify(dataToSave);
    }

    return fetch(_url, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            // console.log("\ncontent-type", response.headers.get("content-type"));
            return response.json();
        })
        .catch((error) => {
            console.error(
                "!!! There was a problem saving/retrieving the data:",
                error
            );
        });
};

function verifyCaptcha(token) {
    console.log('Token received from reCAPTCHA:', token);

    const recapchaBlock = document.querySelector('.banner-block.recapcha');
    const vole_coin_id = recapchaBlock.getAttribute('data-id');

    // Проверка: если id не найден
    if (!vole_coin_id) {
        console.error('Ошибка: data-id отсутствует в .banner-block.recapcha');
        grecaptcha.reset(); // Сбрасываем капчу
        return;
    }

    // Отправить запрос на сервер
    request("/voting/", "POST", { vole_coin_id, token })
        .then((data) => {
            // Скрыть капчу
            recapchaBlock.classList.remove('open');

            if (data.vote) {
                console.log('Голос записан.');

                // Обновить интерфейс
                document.querySelector(`button.js-vote[data-id="${vole_coin_id}"]`).innerText = "Voted";
                document.querySelector(`button.js-vote[data-id="${vole_coin_id}"]`).classList.add('voted');

                document.querySelectorAll(`.js-all_vote-${vole_coin_id}`).forEach(elm => elm.innerText = data.vote);
            } else if (data.status) {
                const bannerBlock = document.querySelector('.banner-block.js-votes-banner');
                bannerBlock.classList.add('open');
                bannerBlock.querySelector('.banner-block__title').innerText = data.status;
            }

            // Сбрасываем ReCAPTCHA для возможности прохождения повторно
            grecaptcha.reset();

        })
        .catch((err) => {
            console.error('Ошибка выполнения запроса:', err);

            // Сбрасываем капчу даже в случае ошибки для возможности повторного ввода
            grecaptcha.reset();
        });
}

// =====================================================================================================================


function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const cookieArr = document.cookie.split(';');
    for (let i = 0; i < cookieArr.length; i++) {
        const cookiePair = cookieArr[i].split('=');
        const cookieName = cookiePair[0].trim();
        if (cookieName === name) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

document.getElementById('accept-cookie').addEventListener('click', function () {
    // Скрыть окно куки
    document.getElementById('cookie-banner').classList.remove('open');

    // Сохранить информацию о согласии пользователя в куки на 30 дней
    setCookie('cookieAccepted', 'true', 30);
});


window.addEventListener('load', () => {
    // Проверить, было ли уже согласие пользователя
    const cookieAccepted = getCookie('cookieAccepted');
    if (cookieAccepted === 'true') {
        document.getElementById('cookie-banner').classList.remove('open');
    }
});
