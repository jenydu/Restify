from django import forms
from ..models import Bank

class CreateBankForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=200, required=True)
    inst_num = forms.CharField(max_length=200, required=True)
    swift_code = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']

    def clean(self):
        cleaned_data = super().clean()

        # Check if all fields are filled
        for field in cleaned_data:
            if not cleaned_data[field]:
                self.add_error(field, 'This field is required')
        return cleaned_data