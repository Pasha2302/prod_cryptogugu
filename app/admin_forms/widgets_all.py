from django.forms.widgets import ClearableFileInput


class NoClearableFileInput(ClearableFileInput):
    clear_checkbox_label = None  # Убирает текст для чекбокса (на всякий случай)
    initial_text = "Текущий файл"  # (не обязательно: кастомизируем текст для существующего файла)
    template_name = "app/admin/widgets/custom_file_input.html"  # Если нужно кастомизировать HTML виджета

    def __init__(self, attrs=None):
        super().__init__(attrs)

