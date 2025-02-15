from django import forms

# from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe

from app.models_db.coin import Coin

from django.forms.widgets import ClearableFileInput


class NoClearableFileInput(ClearableFileInput):
    clear_checkbox_label = None  # Убирает текст для чекбокса (на всякий случай)
    initial_text = "Текущий файл"  # (не обязательно: кастомизируем текст для существующего файла)
    template_name = "app/admin/widgets/custom_file_input.html"  # Если нужно кастомизировать HTML виджета

    def __init__(self, attrs=None):
        super().__init__(attrs)


class CoinAdminForm(forms.ModelForm):
    remove_coin_img = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Coin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CoinAdminForm, self).__init__(*args, **kwargs)
        # Назначаем новый виджет для поля path_coin_img
        self.fields['path_coin_img'].widget = NoClearableFileInput()

        # if self.instance and self.instance.pk:
        #     if self.instance.path_coin_img:
        #         self.fields['path_coin_img'].help_text = mark_safe(
        #             f'<img src="{self.instance.path_coin_img.url}" style="max-width: 200px; max-height: 200px;" />')

    def save(self, commit=True):
        instance = super(CoinAdminForm, self).save(commit=False)
        if self.cleaned_data.get('remove_coin_img') and instance.path_coin_img:
            instance.path_coin_img.delete()  # Удаляет файл из файловой системы

            instance.path_coin_img = None

        if commit:
            instance.save()
        return instance

