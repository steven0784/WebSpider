from django import forms

from .models import Site, CrawledData
from django.contrib.auth.models import User

class AddSiteForm(forms.ModelForm):
    #name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Name', max_length=120)
    class Meta:
        model = Site
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Url'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keywords (separate by ",")'}),
        }
        fields = {'name', 'keywords', 'url'}
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class CrawledDataForm(forms.ModelForm):
    class Meta:
        model = CrawledData
        fields = '__all__'
