from django import forms
from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='댓글', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['body']