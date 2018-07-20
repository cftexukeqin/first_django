from django import forms
from apps.forms import FormMixin
from .models import Comment

class CommentForm(forms.Form,FormMixin):
    content = forms.CharField()
    news_id = forms.CharField()