from django import forms
from django.db.models import fields
from .models import BlogComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('full_name', 'email', 'subject', 'message')
