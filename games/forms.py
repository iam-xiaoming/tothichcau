from django import forms
from .models import Game, Rating
from game_features.models import Category
from django.forms import CheckboxSelectMultiple
from django.core.exceptions import ValidationError


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'price', 'discount', 'publisher', 'release_date', 'image', 'categories']
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    
    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')
        
        if categories and categories.count() > 4:
            raise ValidationError({'categories': "Cannot select more than 4 categories."})
        return cleaned_data
    
    
class UserRating(forms.ModelForm):
    score = forms.IntegerField(min_value=0, max_value=10, widget=forms.NumberInput(attrs={
        'placeholder': 'Score',
        'style': 'color: #b7b7b7; background: #202021; height: 50px; margin-bottom: 15px; font-size: 15px;',
        'class': 'no-arrows'
    }))
    class Meta:
        model = Rating
        fields = ['score']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.game = kwargs.pop('game', None)
        self.comment = kwargs.pop('comment', None)
        
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        rating = super().save(commit=False)
        if self.user:
            rating.user = self.user
        if self.game:
            rating.game = self.game
        if self.comment:
            rating.comment = self.comment
        if rating:
            rating.save()
        return rating
            
        