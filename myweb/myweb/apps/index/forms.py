from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Quote, Author, Tag, UserProfile


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='Email',max_length=100,required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    agree_to_rules = forms.BooleanField(label='Agree to the rules', required=True)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']

class QuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    tag_custom = forms.CharField(max_length=150, required=False, label='Custom Tag')

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tag']
        
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email')
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})