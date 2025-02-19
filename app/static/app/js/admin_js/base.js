// Функция для преобразования строки в объект Date (с учётом вашего формата)
function parseDate(dateStr) {
    // Убираем точки (например, "Feb." -> "Feb")
    const cleanedDateStr = dateStr.replace(/\./g, '');

    // Преобразуем строку в объект даты, добавляя явный парсер
    const dateObj = new Date(Date.parse(cleanedDateStr));

    return dateObj;
}

// Форматирование даты в строку в формате "YYYY-MM-DD HH:mm:ss"
function formatDate(dateStr) {
    if (!dateStr) return ""; // Если строки нет, возвращаем пустую строку

    const dateObj = parseDate(dateStr); // Парсим строку даты
    console.log("Data Object: ", dateObj); // Добавляем отладочный вывод

    // Проверяем, корректно ли создана дата
    if (isNaN(dateObj)) return dateStr; // Если объект даты некорректный, возвращаем оригинальный текст

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


// Выполняем скрипт после загрузки страницы
document.addEventListener('DOMContentLoaded', function () {
    console.log("[Info] Custom script loaded: base.js");

    updateFieldDates(); // Обновляем формат времени в полях
});

