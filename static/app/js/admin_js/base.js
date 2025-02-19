


// Функция для форматирования даты в 24-часовом формате (YYYY-MM-DD HH:mm:ss)
function formatDate(dateStr) {
    if (!dateStr) return ""; // Если строки нет, возвращаем пустую строку

    const dateObj = new Date(dateStr); // Преобразуем строку в объект Date

    console.log("Data Object: ", dateObj);

    // Проверяем, корректно ли создана дата
    if (isNaN(dateObj)) return dateStr; // Если дата некорректная, возвращаем оригинальный текст

    // Форматируем дату вручную
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, '0'); // Месяц (с учетом индексации с 0)
    const dd = String(dateObj.getDate()).padStart(2, '0');
    const hh = String(dateObj.getHours()).padStart(2, '0');
    const mi = String(dateObj.getMinutes()).padStart(2, '0');
    const ss = Stri
    ng(dateObj.getSeconds()).padStart(2, '0');

    return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}

// Функция для получения всех элементов с датами
function getFieldsDate() {
    // Ищем элементы с классами для полей start_time и end_time
    const startTimeFields = document.querySelectorAll('.field-start_date');
    const endTimeFields = document.querySelectorAll('.field-end_date');

    return [...startTimeFields, ...endTimeFields]; // Возвращаем массив найденных элементов
}

// Функция для обновления текста в элементах
function updateFieldDates() {
    const dateFields = getFieldsDate(); // Получаем поля с датами

    dateFields.forEach((field) => {
        console.log("\nField: ", field);
        console.log("Field Text: ", field.textContent);
        if (field && field.textContent) { // Проверяем, что поле существует и имеет текст
            field.textContent = formatDate(field.textContent.trim()); // Форматируем текстовое содержимое
        }
    });
}


// Выполняем скрипт после загрузки страницы
document.addEventListener('DOMContentLoaded', function () {
    console.log("[Info] Custom script loaded: base.js");

    updateFieldDates(); // Обновляем формат времени в полях
});
