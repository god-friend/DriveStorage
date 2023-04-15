from .models import User, UploadedFiles
from django import forms
from django.contrib.auth import authenticate

class SignUp(forms.Form):
    __form_attr = {"class": "form-control"}
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=__form_attr))
    firstname = forms.CharField(label="FirstName", widget=forms.TextInput(attrs=__form_attr))
    lastname = forms.CharField(label="LastName", widget=forms.TextInput(attrs=__form_attr))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs=__form_attr))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs=__form_attr))
    confirm_pass = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs=__form_attr))

    def clean(self):
        cleaned_data = super(SignUp, self).clean()
        print(cleaned_data)
        if cleaned_data['pwd'] != cleaned_data['confirm_pass']:
            self.add_error("confirm_pass", "Password Doesn't Match")
        
        return cleaned_data
    

class LoginForm(forms.Form):
    __form_attr = {"class": "form-control"}
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=__form_attr))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs=__form_attr))


class UploadForm(forms.ModelForm):
    
    class Meta:
        model = UploadedFiles
        fields = ['file']
        widgets = {
            "file": forms.FileInput(attrs={"class": "form-control", "multiple": True}),
        }
    
