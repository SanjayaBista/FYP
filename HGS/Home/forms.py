from django.forms import ModelForm, TextInput
from django import forms
from .models import Comment

class FormComment(ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'review') 
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title'
                }),
            'review': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'review'
                })
        } 
      