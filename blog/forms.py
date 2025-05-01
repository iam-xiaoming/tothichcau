from django import forms
from .models import Post, Category, Tag
from django.forms import CheckboxSelectMultiple

class PostAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Post
        fields = ['user', 'title', 'category', 'tags', 'content']
        
        
class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Category"
    )
    tags = forms.CharField(
        required=False,
        help_text="Add tags separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas...'})
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter an engaging title...',
            'maxlength': 200
        })
    )
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter your post content...',
        'rows': 10
    }))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']