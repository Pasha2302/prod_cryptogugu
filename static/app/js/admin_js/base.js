// Функция для очистки и исправления строки времени
function cleanTimeString(dateStr) {
    if (!dateStr) return "";

    // Приводим a.m./p.m. к AM/PM перед удалением точек
    let cleanedDateStr = dateStr
        .replace("a.m.", "AM") // Приводим a.m. к AM
        .replace("p.m.", "PM") // Приводим p.m. к PM
        .replace(/\./g, "");   // Убираем точки

    // Проверяем, есть ли минуты в строке времени (например, "6 AM" или "6:00 AM")
    const timeRegex = /(\d+:\d+)\s*(AM|PM)$/i; // Ищем часы с минутами
    if (!timeRegex.test(cleanedDateStr)) {
        // Если минуты отсутствуют, добавляем их
        cleanedDateStr = cleanedDateStr.replace(/(\d+)\s+(AM|PM)$/i, "$1:00 $2");
    }

    return cleanedDateStr;
}

// Функция для обработки строки даты
function parseDate(dateStr) {
    if (!dateStr) return null;

    // Исправляем строку времени
    const cleanedDateStr = cleanTimeString(dateStr);
    console.log("Cleaned Date String: ", cleanedDateStr); // Для отладки

    // Пробуем создать объект Date
    const dateObj = new Date(cleanedDateStr);

    // Проверяем, корректен ли объект даты
    return isNaN(dateObj) ? null : dateObj;
}

// Функция для форматирования даты в "YYYY-MM-DD HH:mm:ss"
function formatDate(dateStr) {
    if (!dateStr) return ""; // Если строки нет, возвращаем пустую строку

    const dateObj = parseDate(dateStr); // Парсим строку даты
    console.log("Data Object: ", dateObj); // Для отладки

    // Если объект даты некорректен, возвращаем изначальную строку
    if (!dateObj) {
        console.warn("Failed to parse date: ", dateStr);
        return dateStr;
    }

    // Форматируем дату в "YYYY-MM-DD HH:mm:ss"
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, "0"); // Месяц
    const dd = String(dateObj.getDate()).padStart(2, "0"); // День
    const hh = String(dateObj.getHours()).padStart(2, "0"); // Часы
    const mi = String(dateObj.getMinutes()).padStart(2, "0"); // Минуты
    const ss = String(dateObj.getSeconds()).padStart(2, "0"); // Секунды

    return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}

// Получаем все элементы с датами
function getFieldsDate() {
    return [
        ...document.querySelectorAll("#result_list .field-start_time"),
        ...document.querySelectorAll("#result_list .field-end_time"),
        ...document.querySelectorAll("#result_list .field-start_date"),
        ...document.querySelectorAll("#result_list .field-end_date"),
        ...document.querySelectorAll("#result_list .field-uploaded_at"),
    ];
}

// Обновляем текст в найденных элементах
function updateFieldDates() {
    const dateFields = getFieldsDate();
    console.log("\nData Fields: ", dateFields);

    // Для каждого поля обновляем текстовое содержимое
    dateFields.forEach((field) => {
        console.log("Field: ", field);
        console.log("Field Text: ", field.textContent.trim());
        if (field && field.textContent) {
            field.textContent = formatDate(field.textContent.trim());
        }
    });
}

// Выполняем после загрузки страницы
window.onload = function () {
    console.log("[Info] Custom script loaded: base.js");
    updateFieldDates(); // Обновляем формат времени
};