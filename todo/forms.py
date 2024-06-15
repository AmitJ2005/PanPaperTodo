from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Learning
from .models import Profile

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class LearningForm(forms.ModelForm):
    class Meta:
        model = Learning
        fields = ['content', 'date']  # Include 'date' field
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']