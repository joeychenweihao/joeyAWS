# forum/forms.py
from django import forms
from .models import Post, Comment, User,TempRegister, Competition
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = TempRegister
        fields = ['email', 'username', 'name', 'date_of_birth']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'start_date', 'end_date', 'registration_fee', 'prize_pool', 'status', 'image']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")