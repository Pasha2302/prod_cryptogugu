from django import forms

from app.admin_forms.widgets_all import NoClearableFileInput
from app.models_db.coin import Market


class MarketAdminForm(forms.ModelForm):

    class Meta:
        model = Market
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Пример назначения кастомного виджета для поля, если это необходимо
        if 'image' in self.fields:
            self.fields['image'].widget = NoClearableFileInput()



