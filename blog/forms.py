from django import forms
from .models import Post, Category, Tag
from django.forms import CheckboxSelectMultiple
import re

class PostAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Post
        fields = ['user', 'title', 'categories', 'tags', 'content']
        