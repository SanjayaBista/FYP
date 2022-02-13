from django.forms import ModelForm
from django import forms
from .models import Comment

class FormComment(ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'review', 'rating')