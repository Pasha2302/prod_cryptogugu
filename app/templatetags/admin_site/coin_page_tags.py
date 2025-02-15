from django import template

register = template.Library()


@register.simple_tag
def generate_classes_form_row(line):
    """ Генерирует строку классов для form-row """
    # print(f"[DEBUG] Line object: {line}")  # Для отладки данных line

    classes = ["form-row"]
    # Проверяем наличие атрибутов в 'line'
    fields = getattr(line, 'fields', [])  # Если fields отсутствует, используем пустой список
    errors = line.errors() if getattr(line, 'errors') else False
    # print(f"[DEBUG coin_page_tags.py (15)] Field errors: {errors} /  {type(errors)=}")

    has_visible_field = getattr(line, 'has_visible_field', True)

    # Добавляем класс 'errors', если есть ошибки и только одно поле
    if len(fields) == 1 and errors:
        classes.append("errors")

    # Добавляем класс 'hidden', если нет видимого поля
    if not has_visible_field:
        classes.append("hidden")

    # Добавляем имя каждого поля как класс
    for field in line:
        if isinstance(field, dict):  # Если поле представлено как словарь
            if "field" in field and "name" in field["field"]:
                classes.append(f"field-{field['field']['name']}")
        elif hasattr(field, 'field') and hasattr(field.field, 'name'):  # Если поле — объект
            classes.append(f"field-{field.field.name}")

    return " ".join(classes)


@register.simple_tag
def generate_classes_flex_container(line, field):
    """ Генерирует строку классов для flex-container """
    # print(f"[DEBUG] Field: {field} | Type: {type(field)}")
    # print(f"[DEBUG] Line: {line} | Type: {type(line)}")
    # print(f"[DEBUG] AdminField: {field.__dict__}")

    classes = ["flex-container"]

    # Добавляем класс 'fieldBox', если line содержит более одного поля
    if len(line.fields) != 1:
        classes.append("fieldBox")

    # Добавляем класс для имени поля
    if hasattr(field.field, 'name'):
        classes.append(f"field-{field.field.name}")

    # Проверяем, есть ли ошибки
    if not field.is_readonly and hasattr(field, 'errors'):  # Проверяем наличие метода errors
        field_errors = field.errors()  # Вызов метода errors, чтобы получить реальные данные
        if field_errors:  # Если есть реальные ошибки
            print(f"[DEBUG coin_page_tags.py (59)] Field errors: {field_errors}")
            classes.append("errors")

    # Класс 'hidden', если поле скрыто
    if hasattr(field.field, 'is_hidden') and field.field.is_hidden:
        classes.append("hidden")

    # Класс 'checkbox-row', если поле - флажок
    if hasattr(field, 'is_checkbox') and field.is_checkbox:
        classes.append("checkbox-row")

    return " ".join(classes)


