from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=120, required=True)
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(max_length=120, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
        'email' : {
            'invalid' : "Enter a valid email address",
        },
        'username' : {
            "required": "This field is required",
        },
        'password1' : {
            "required": "This field is required",
        },
        'password2' : {
            "required": "This field is required",
        },
    }
    

    def clean(self):
        data = super().clean()
        username = data['username']
        if not username:
            raise forms.ValidationError({'username' : "This field is required"})
        password1 = data['password1']
        if not password1:
            raise forms.ValidationError({'password1' : "This field is required"})
        password2 = data['password2']
        if not password1:
            raise forms.ValidationError({'password2' : "This field is required"})

        if password1 != password2:
            raise ValidationError("The two password fields didn't match")
        if len(password1) < 8:
            raise ValidationError("This password is too short. It must contain at least 8 characters")
        # if User.objects.filter(username=data['username']).exists():
        #     raise ValidationError("A user with that username already exists")

        return data
    
    def save(self, commit=True):
    # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username','password']
    def clean(self):
        data = super().clean()
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError({
                'username' : 'Username or password is invalid'}
            )
        data['user'] = user
        return data
    
class GetProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(max_length=120, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(max_length=120, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
        'email' : {
            'invalid' : "Enter a valid email address",
        },
    }
    def clean(self):
        data = super().clean()

        password1 = data['password1']
        password2 = data['password2']
        if password1:

            if password1 != password2:
                raise ValidationError("The two password fields didn't match")
            if len(password1) < 8:
                raise ValidationError("This password is too short. It must contain at least 8 characters")
        return data