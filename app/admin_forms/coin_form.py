from django import forms

# from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe

from app.admin_forms.widgets_all import NoClearableFileInput
from app.models_db.coin import Coin, BaseCoin


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


class BaseCoinAdminForm(forms.ModelForm):

    class Meta:
        model = BaseCoin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Пример назначения кастомного виджета для поля, если это необходимо
        if 'path_coin_img' in self.fields:
            self.fields['path_coin_img'].widget = NoClearableFileInput()

        if 'path_chain_img' in self.fields:
            self.fields['path_chain_img'].widget = NoClearableFileInput()

