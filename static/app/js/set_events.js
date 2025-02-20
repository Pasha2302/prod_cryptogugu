"use strict";
import getDropdownManager from "./moduls/dropdown.js";
import { requestServer } from "./moduls/modul_index.js";



var setThemeEvent = () => {
    var theme = document.querySelector("body");
    var currentTheme = localStorage.getItem('theme_site');
    if (currentTheme) theme.setAttribute("data-theme", currentTheme);

    var setTheme = (name) => {
        theme.setAttribute("data-theme", name);
        localStorage.setItem("theme_site", name);
        requestServer("set-theme-site/", "POST", { 'theme_site': name }
        ).then((data) => console.log('\nEvent Set Theme:', data));
    };

    var toggleTheme = () => {
        if (theme.getAttribute("data-theme") === "light") setTheme("dark");
        else setTheme("light");
    };

    var themeButtons = [
        document.querySelector(".header__theme"),
        document.querySelector(".footer__theme"),
        document.querySelector(".header__theme-mob"),
    ];

    themeButtons.forEach((button) => {
        if (button) {
            button.addEventListener("click", toggleTheme);
        }
    });
};


var setMobileMenu = () => {
    document.querySelectorAll(".mobile-menu__link-sub").forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            link.parentElement.classList.toggle("active");
        });
    });

    document.querySelector(".header__burger").addEventListener("click", (e) => {
        e.target.classList.toggle("active");
        document.querySelector(".mobile-menu").classList.toggle("open");
        document.querySelector("body").classList.toggle("body_hidden");
    });
};


var setSearchInput = (dropdownManager) => {
    var searchInput = document.querySelector("#header-search-input");
    var headerSearch = document.querySelector(".header__search");

    searchInput.addEventListener("input", (_) => {
        if (searchInput.value.length > 0) {
            headerSearch.classList.add("open");
        } else {
            headerSearch.classList.remove("open");
        }
    });

    dropdownManager.closeOnClickOutside(".header__search", "open");
};

// ===================================================================================================================


function setEventHeaderSearchMobile() {
    document.addEventListener('click', (e) => {
        const withinBoundaries = e.composedPath().includes(document.querySelector('.header__search'));
        try {
            !withinBoundaries ? document.querySelector('.header__search').classList.remove('open') : !1
        } catch (error) { }
    });

    document.addEventListener('click', (e) => {
        const withinBoundaries = e.composedPath().includes(document.querySelector('.header__search'));

        try {
            !withinBoundaries ? document.querySelector('.header__search').classList.remove('active') : false;
        } catch (error) {

        }
    });

    document.querySelector('.header__search').addEventListener('click', () => {
        document.querySelector('.header__search').classList.add('active')
    });
}

// ===================================================================================================================


var setCoinTableScroll = () => {
    document.querySelectorAll(".coin-table").forEach((item) => {
        // console.log(item.getElementsByTagName('table')[0].offsetWidth);
        // console.log(item.offsetWidth);
        let table = item.getElementsByTagName("table");
        if (
            table.length > 0 && table[0].offsetWidth - 10 >=
            item.offsetWidth
        ) {
            item.classList.add("coin-table_scroll");
            // console.log(1);
        } else {
            item.classList.remove("coin-table_scroll");
            // console.log(2);
        }
    });
};


var setEventLanguage = (dropdownManager) => {
    var dropdownConfigs = [
        {
            triggerSelector: ".header__lang-current",
            targetSelector: ".header__lang",
            className: "open",
        },
        {
            triggerSelector: ".header__lang-current-mob",
            targetSelector: ".header__lang-mob",
            className: "open",
        },
        {
            triggerSelector: ".footer__lang-current",
            targetSelector: ".footer__lang",
            className: "open",
        },
    ];

    dropdownConfigs.forEach(({ triggerSelector, targetSelector, className }) => {
        dropdownManager.toggleClassOnClick(
            triggerSelector,
            targetSelector,
            className
        );
        dropdownManager.closeOnClickOutside(targetSelector, className);
    });
};


var setBannerBlockClose = () => {
    document.querySelectorAll(".banner-block__item-close").forEach((item) => {
        item.addEventListener("click", (e) => {
            e.target.closest(".banner-block").classList.remove("open");
        });
    });

    document.querySelectorAll(".banner-block__overlay").forEach((item) => {
        item.addEventListener("click", (e) => {
            e.target.closest(".banner-block").classList.remove("open");
        });
    });
};


var getUserId = () => {
    fetch("/get-user-id/")
        .then((response) => response.json())
        .then((data) => {
            document.cookie = `userId=${data.user_id}; path=/`;
        })
        .catch((error) => console.error("Error fetching unique ID:", error));
};


var setLanguage = () => {
    document.querySelectorAll('[data-lang-code]').forEach(function (item) {
        item.addEventListener("click", function (event) {
            console.log("\nLanguage Set Event ...")
            event.preventDefault();
            var langCode = item.getAttribute("data-lang-code");
            var currentPath = window.location.pathname;
            var pathParts = currentPath.split("/").filter(function (part) {
                return part !== "";
            });

            // Проверяем, является ли первый элемент языковым кодом
            if (
                pathParts.length > 0 &&
                pathParts[0] in { en: "", ru: "", es: "", pt: "", "zh-hans": "" }
            ) {
                pathParts.shift();
            }

            // Формируем новый путь
            var newPath =
                "/" + (langCode === "en" ? "" : langCode + "/") + pathParts.join("/");
            window.location.href = newPath;
        });
    });
};


// ================================================================================================================ //

function changeList(styleListStep1, styleListStep2, _type) {
    var step1 = document.querySelector('.header__search-list-step1');
    var step2 = document.querySelector('.header__search-list-step2');

    step1.style.display = styleListStep1;
    step2.style.display = styleListStep2;

    var addData = (title, subclass) => {
        step2.querySelector('.header__search-list-label').innerText = title;

        step1.querySelectorAll(`a.header__search-list-item.${subclass}`).forEach(link => {
            const clonedLink = link.cloneNode(true);
            clonedLink.classList.add('cloned-item');
            clonedLink.style.display = 'block';
            step2.appendChild(clonedLink);
        });
    }

    if (styleListStep2 === 'block') {
        // Удаление всех динамически добавленных элементов
        step2.querySelectorAll('.cloned-item').forEach(link => link.remove());

        (_type === 'coin') ? addData('Coins', 'js-coins') : (_type === 'airdrop') ? addData('Airdrops', 'js-airdrops') : null;

    };

}


function clearSearchHeader() {
    var step1 = document.querySelector('.header__search-list-step1');
    var step2 = document.querySelector('.header__search-list-step2');
    step1.querySelectorAll('.header__search-list-item.js-coins').forEach(link => link.remove());
    step1.querySelectorAll('.header__search-list-item.js-airdrops').forEach(link => link.remove());
    step1.querySelector('.header__search-list-all.js-coins').innerText = '';
    step1.querySelector('.header__search-list-all.js-airdrops').innerText = '';
    step2.querySelectorAll('.cloned-item').forEach(link => link.remove());
}

var setEventSearchListAllAirdrops = () => {
    document.querySelector('.header__search-list-all.js-airdrops').addEventListener('click', function () {
        changeList('none', 'block', 'airdrop');
    });
}


var setEventSearchListAllCoins = () => {
    document.querySelector('.header__search-list-all.js-coins').addEventListener('click', function () {
        changeList('none', 'block', 'coin');
    });
}


var setEventBackListStep1 = () => {
    document.querySelector('.header__search-list-back').addEventListener('click', function () {
        changeList('block', 'none');
    })
}

var setEventSearchList = () => {
    document.querySelector('.header__search-reset').addEventListener('click', () => {
        clearSearchHeader();
    })
    setEventBackListStep1();
    setEventSearchListAllCoins();
    setEventSearchListAllAirdrops();
}

function debounce(func, delay) {
    let timeoutId;
    console.log("\nColl debounce() timeoutId:", timeoutId);
    return function (...args) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
};

var setEventSearchHeader = () => {
    var searchInput = document.querySelector('#header-search-input');

    searchInput.addEventListener('input', debounce(function (event) {
        console.log('\nsearchInput.addEventListener()')
        // var query = event.target.value;
        var query = this.value;
        if (query.length > 0) {
            requestServer("/header-search-component/", "POST", { query }
            ).then((data) => {
                // console.log('\nEvent Search Header:', data);
                var targetBlock = document.querySelector('.header__search-list');
                targetBlock.innerHTML = data.coins_html;
                setEventSearchList();
            });

        } else clearSearchHeader();

    }, 1000));
};

// ================================================================================================================================================


var setEventVotes = () => {
    $('body').on('click', 'button.js-vote', function () {
        var vole_coin_id = $(this).attr('data-id');

        // Показываем блок с капчей
        $('.banner-block.recapcha').addClass('open').attr('data-id', vole_coin_id);
    });
}

function verifyCaptcha(token) {
    console.log("\nVerify Captcha token: ", token);
    // Найти блок recapcha и получить id монеты
    var recapchaBlock = document.querySelector('.banner-block.recapcha');
    var vole_coin_id = recapchaBlock.getAttribute('data-id');

    // Отправить запрос на сервер с токеном капчи
    requestServer("/voting/", "POST", { vole_coin_id, token })
        .then((data) => {
            // После успешного ответа закрыть блок капчи и изменить текст кнопки
            recapchaBlock.classList.remove('open'); // Скрыть капчу

            if (data.vote) {
                document.querySelector(`button.js-vote[data-id="${vole_coin_id}"]`).innerText = "Voted";
                document.querySelector(`button.js-vote[data-id="${vole_coin_id}"]`).classList.add('voted');

                document.querySelectorAll(`.js-all_vote-${vole_coin_id}`).forEach(elm => elm.innerText = data.vote);

            } else if (data.status) {
                var bannerBlock = document.querySelector('.banner-block.js-votes-banner');
                bannerBlock.classList.add('open');
                bannerBlock.querySelector('.banner-block__title').innerText = data.status;
            };

        })
        .catch((err) => {
            console.error("Ошибка выполнения запроса:", err);
        });
}



// var setEventVotes = () => {
//     $('body').on('click', 'button.js-vote', function () {
//         var vole_coin_id = $(this).attr('data-id');
//         // console.log('\nEvent Votes coin_id:', vole_coin_id);
//         // grecaptcha.reset();
//         $('.banner-block.recapcha').addClass('open')

//         requestServer("/voting/", "POST", { vole_coin_id })
//             .then((data) => {
//                 // console.log('\nEvent Votes:', data);
//                 this.classList.add('voted');

//                 if (data.status) {
//                     var bannerBlock = document.querySelector('.banner-block.js-votes-banner');
//                     bannerBlock.classList.add('open');
//                     bannerBlock.querySelector('.banner-block__title').innerText = data.status;
//                 }
//                 else if (data.vote) {
//                     document.querySelectorAll(`.js-all_vote-${vole_coin_id}`).forEach(elm => elm.innerText = data.vote);
//                     // var elmDailyVotes = document.querySelector(`span.js-daily_vote-${vole_coin_id}`);
//                     // elmDailyVotes.innerText = data.daily_vote;
//                 };

//             });

//     });
// }


window.addEventListener("load", () => {
    // window.addEventListener("DOMContentLoaded", () => {
    var dropdownManager = getDropdownManager();
    getUserId();

    setEventLanguage(dropdownManager);
    setLanguage()
    setThemeEvent();
    setMobileMenu();
    setSearchInput(dropdownManager);
    setBannerBlockClose();

    setEventSearchHeader();
    setEventVotes();

    setEventHeaderSearchMobile();

});


window.addEventListener("resize", () => {
    // We execute the same script as before

    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
    setCoinTableScroll();
});
