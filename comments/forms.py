from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta: # 大写字母
        model = Comment
        fields = ['name','email','url','text']