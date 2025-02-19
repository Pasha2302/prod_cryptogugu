from django import forms

from app.admin_forms.widgets_all import NoClearableFileInput
from app.models_db.coin import Chain


class ChainAdminForm(forms.ModelForm):

    class Meta:
        model = Chain
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Пример назначения кастомного виджета для поля, если это необходимо
        if 'path_chain_img' in self.fields:
            self.fields['path_chain_img'].widget = NoClearableFileInput()

