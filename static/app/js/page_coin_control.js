"use strict";
import {
    getDataPromotedCoinsTable,
} from "./moduls/modul_index.js";


function copyContractAddress() {
    $(document).on("click", ".js-copy", function (e) {
        e.preventDefault(); // Предотвращаем стандартное поведение (если у кнопки есть другое действие)

        var $this = $(this); // Сохраняем объект кнопки

        // Копируем текст из атрибута `data-copy`
        navigator.clipboard.writeText($this.attr("data-copy")).then(function () {
            // Добавляем элемент с текстом "Copied"
            $this.append('<span class="copied">Copied</span>');

            // Показываем эффект появления
            $this.find(".copied").fadeIn(function () {
                // Скрываем текст через 300 мс
                setTimeout(function () {
                    $this.find(".copied").fadeOut(function () {
                        $(this).remove(); // Удаляем текст после скрытия
                    });
                }, 300);
            });
        }).catch(function (err) {
            console.error("Ошибка копирования: ", err);
        });
    });
}


function showMoreAbout() {
    const readMoreButtons = document.querySelectorAll(".read-more"); // Находим все кнопки "Read More"

    readMoreButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const parentDiv = this.closest(".token-card__text"); // Ищем родительский div
            if (parentDiv) {
                parentDiv.classList.add("open"); // Добавляем класс "open" родителю
            }
            this.style.display = "none"; // Скрываем кнопку
        });
    });

}


$('body').on('click', '.token-card__chart-button', function() {
    if ($(this).hasClass('used')) {
        $(this).html('Hide');
        $('#dexscreener-embed').slideDown();
        $(this).removeClass('used')
    } else {
        $(this).html('Show');
        $('#dexscreener-embed').slideUp();
        $(this).addClass('used')
    }
});


window.addEventListener('load', () => {
    console.log("\nPage Coin Control.")
    getDataPromotedCoinsTable();

    copyContractAddress();
    showMoreAbout();

});
