from dataclasses import field
from tkinter import W
from django import forms
from .models import Customer


class RegisterForm(forms.ModelForm):

    phoneNumber = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ['first_name','last_name', 'email']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
