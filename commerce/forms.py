from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from commerce.models import Address, OrderSpecial

class UsersCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',]

class AddAddress(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    company = forms.CharField(label='Raison social', required=False)
    company_form = forms.CharField(label='Forme', required=False)
    cin = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    
    class Meta:
        model = Address
        exclude = ['user']

class AddParticularAddress(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    cin = forms.CharField(required=False)
    
    company = forms.CharField(label='Raison social', required=False)
    company_form = forms.CharField(label='Forme', required=False)
    cin = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    
    class Meta:
        model = Address
        exclude = ['user', 'company', 'company_form', 'nif']

class AddSocietyAddress(forms.ModelForm):
    company = forms.CharField(label='Raison social', required=False)
    company_form = forms.CharField(label='Forme', required=False)
    nif = forms.CharField(required=False)
    
    company = forms.CharField(label='Raison social', required=False)
    company_form = forms.CharField(label='Forme', required=False)
    cin = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    
    class Meta:
        model = Address
#         fields = '__all__'
        exclude = ['user', 'gender', 'first_name', 'last_name', 'cin']
        

class OrderSpecialForm(forms.ModelForm):
#     name = forms.CharField(max_length=100, required=True)
#     short_desc = forms.CharField(max_length=100, required=False)
#     long_desc = forms.CharField(max_length=100, required=False)
     
    class Meta:
        model = OrderSpecial
        fields = ['name', 'short_desc', 'long_desc', 'quantity', 'thumbnail',]
        exclude = ['user']