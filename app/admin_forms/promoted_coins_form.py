from django import forms


class PromotedCoinsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if (start_date and not end_date) or (end_date and not start_date):
            raise forms.ValidationError("Both start date and end date are required if one is filled.")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

