from django import forms
from django.core.exceptions import ValidationError
from ..models import Branch


class CreateBranchForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    address = forms.CharField(max_length=200, required=True)
    transit_num = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    capacity=forms.IntegerField(required=False)

    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']
        error_messages = {
        'email' : {
            'invalid' : "Enter a valid email address",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            if field != 'capacity' and not cleaned_data[field]:
                self.add_error(field, 'This field is required')
        return cleaned_data