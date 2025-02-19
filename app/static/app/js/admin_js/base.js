// Функция для преобразования строки в объект Date
function parseDate(dateStr) {
    if (!dateStr) return null;

    // Убираем точки из сокращений и преобразуем AM/PM к удобному виду
    const cleanedDateStr = dateStr
        .replace(/\./g, '') // Убираем точки
        .replace('a.m.', 'AM') // Приводим AM/PM к валидным значениям
        .replace('p.m.', 'PM'); 

    console.log("Cleaned Date String: ", cleanedDateStr); // Для отладки

    // Регулярное выражение для парсинга строки формата "Feb 26, 2025, 6 AM"
    const match = cleanedDateStr.match(/^([a-zA-Z]+) (\d+), (\d+), (\d+):?(\d+)? (AM|PM)$/);
    if (match) {
        const [, month, day, year, hourRaw, minuteRaw = '0', period] = match;

        // Преобразуем месяц в номер (Jan = 1, Feb = 2, ...)
        const monthMap = {
            Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
            Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11
        };
        const monthIndex = monthMap[month.charAt(0).toUpperCase() + month.slice(1).toLowerCase()];

        if (monthIndex === undefined) return null; // Некорректный месяц → прерываем

        // Преобразуем AM/PM формат времени в 24-часовой
        let hour = parseInt(hourRaw, 10);
        if (period === 'PM' && hour !== 12) hour += 12; // Добавляем 12 часов для PM
        if (period === 'AM' && hour === 12) hour = 0;   // Устанавливаем 0 для 12 AM
        const minute = parseInt(minuteRaw, 10);

        // Создаём объект Date
        return new Date(year, monthIndex, day, hour, minute);
    }

    // Если это уже стандартный ISO-формат, попробуем парсинг напрямую
    const dateObj = new Date(cleanedDateStr);
    return isNaN(dateObj) ? null : dateObj;
}


// Форматирование даты в строку "YYYY-MM-DD HH:mm:ss"
function formatDate(dateStr) {
    if (!dateStr) return ""; // Если строки нет, возвращаем пустую строку

    const dateObj = parseDate(dateStr); // Парсим строку даты
    console.log("Data Object: ", dateObj); // Для отладки

    // Проверяем, создана ли дата корректно
    if (!dateObj) {
        console.warn("Failed to parse date: ", dateStr);
        return dateStr; // Возвращаем исходный текст, если дата некорректна
    }

    // Форматируем дату в виде "YYYY-MM-DD HH:mm:ss"
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, '0');
    const dd = String(dateObj.getDate()).padStart(2, '0');
    const hh = String(dateObj.getHours()).padStart(2, '0');
    const mi = String(dateObj.getMinutes()).padStart(2, '0');
    const ss = String(dateObj.getSeconds()).padStart(2, '0');

    return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}


// Функция для получения всех элементов с необходимыми датами
function getFieldsDate() {
    return [
        ...document.querySelectorAll('#result_list .field-start_time'),
        ...document.querySelectorAll('#result_list .field-end_time'),
        ...document.querySelectorAll('#result_list .field-start_date'),
        ...document.querySelectorAll('#result_list .field-end_date'),
        ...document.querySelectorAll('#result_list .field-uploaded_at'),
    ];
}


// Функция для обновления текста в элементах
function updateFieldDates() {
    const dateFields = getFieldsDate();
    console.log("\nData Fields: ", dateFields);

    dateFields.forEach((field) => {
        console.log("Field: ", field);
        console.log("Field Text: ", field.textContent.trim());
        if (field && field.textContent) {
            field.textContent = formatDate(field.textContent.trim());
        }
    });
}


// Запускаем скрипт после полной загрузки страницы
window.onload = function () {
    console.log("[Info] Custom script loaded: base.js");
    updateFieldDates(); // Обновляем формат времени в полях
};
