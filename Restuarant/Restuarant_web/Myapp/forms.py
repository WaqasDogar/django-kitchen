from django.db.models import fields
from .models import *
from django import forms

class userform(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','email','first_name','last_name']
class contactusform(forms.ModelForm):
    class Meta:
        model = contactus
        fields='__all__'
class proform(forms.ModelForm):
    class Meta:
        model = Product
        fields='__all__'