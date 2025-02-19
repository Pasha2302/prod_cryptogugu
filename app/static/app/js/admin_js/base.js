// Функция для преобразования строки в объект Date (с учётом формата AM/PM)
function parseDate(dateStr) {
    if (!dateStr) return null;

    // Убираем точки из сокращений, таких как "Feb." -> "Feb", "a.m." -> "AM", "p.m." -> "PM"
    let cleanedDateStr = dateStr
        .replace(/\./g, '') // Убираем точки
        .replace('a.m.', 'AM') // Приводим AM/PM к валидным значениям
        .replace('p.m.', 'PM');

    console.log("Cleaned Date String: ", cleanedDateStr); // Для отладки

    // Явный разбор формата "Feb 26, 2025, 6 AM"
    const match = cleanedDateStr.match(/([a-zA-Z]+) (\d+), (\d+), (\d+):?(\d+)? (AM|PM)/);
    if (match) {
        const [_, month, day, year, hourRaw, minuteRaw = '0', period] = match;

        // Преобразуем AM/PM время в 24-часовой формат
        let hour = parseInt(hourRaw, 10);
        if (period === 'PM' && hour !== 12) hour += 12;
        if (period === 'AM' && hour === 12) hour = 0;

        const minute = parseInt(minuteRaw, 10);

        // Используем формат Date для представления результата
        return new Date(`${month} ${day}, ${year} ${hour}:${minute}`);
    }

    // Если это уже ISO или другой формат, который понимает JavaScript
    const dateObj = new Date(Date.parse(cleanedDateStr));
    return isNaN(dateObj) ? null : dateObj;
}

// Форматирование даты в строку формата "YYYY-MM-DD HH:mm:ss"
function formatDate(dateStr) {
    if (!dateStr) return ""; // Если строки нет, возвращаем пустую строку

    const dateObj = parseDate(dateStr); // Парсим строку даты
    console.log("Data Object: ", dateObj); // Выводим объект для отладки

    // Проверяем, создался ли корректный объект даты
    if (!dateObj) {
        console.warn("Failed to parse date: ", dateStr);
        return dateStr; // Если дата некорректна, возвращаем оригинальный текст
    }

    // Форматируем дату вручную
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, '0'); // Месяц (с учетом индексации с 0)
    const dd = String(dateObj.getDate()).padStart(2, '0');
    const hh = String(dateObj.getHours()).padStart(2, '0');
    const mi = String(dateObj.getMinutes()).padStart(2, '0');
    const ss = String(dateObj.getSeconds()).padStart(2, '0');

    return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}

// Функция для получения всех элементов с необходимыми датами
function getFieldsDate() {
    // Ищем элементы с классами для полей start_time и end_time
    
    return [
        ...document.querySelectorAll('#result_list .field-start_time'),
        ...document.querySelectorAll('#result_list .field-end_time'),

        ...document.querySelectorAll('#result_list .field-start_date'),
        ...document.querySelectorAll('#result_list .field-end_date'),
        ...document.querySelectorAll('#result_list .field-uploaded_at'),
    ]

}

// Функция для обновления текста в элементах
function updateFieldDates() {
    const dateFields = getFieldsDate(); // Получаем поля с датами
    console.log("\nData Fields: ", dateFields);

    dateFields.forEach((field) => {
        console.log("Field: ", field);
        console.log("Field Text: ", field.textContent);
        if (field && field.textContent) { // Проверяем, что поле существует и имеет текст
            field.textContent = formatDate(field.textContent.trim()); // Форматируем текстовое содержимое
        }
    });
}


// Выполняем скрипт после полной загрузки всех ресурсов страницы
window.onload = function () {
    console.log("[Info] Custom script loaded: base.js");

    updateFieldDates(); // Обновляем формат времени в полях
};
