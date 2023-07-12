from typing import Any
from django import forms
from django.conf import settings

from .models import Post


class PostModelForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = ('title', 'content', 'banner', 'txt_file', 'some_file')