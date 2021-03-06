from django.forms import ModelForm, TextInput
from django import forms
from .models import Comment

class FormComment(ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'review', 'rating') 
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

class SearchQuery(forms.Form):
    search = forms.CharField()
