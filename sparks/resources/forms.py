from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import resources_post,blogPermissionPost

class uploadform(forms.ModelForm):
    file = forms.FileField(required=True)
    class Meta:
        model = resources_post
        fields = ["title","subject","file"]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id' : 'title',
                
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'id':'subject'
            }),
             'file': forms.FileInput(attrs={
                'class': 'form-control',
                'id':'file',
                
            })
        }
    
class blogpost(forms.ModelForm):
    class Meta:
        model = blogPermissionPost
        fields = ["title","content","author","published"]


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists ❌")

        return email