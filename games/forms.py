from django import forms
from .models import Game, Rating, DLC
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
    

class DLCAdminForm(forms.ModelForm):
    class Meta:
        model = DLC
        fields = ['game', 'name', 'description', 'price', 'discount', 'release_date', 'image']
    
    
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
        self.dlc = kwargs.pop('dlc', None)
        self.comment = kwargs.pop('comment', None)
        
        super().__init__(*args, **kwargs)
        
    def clean(self):
        clean_data =  super().clean()
        
        if not (self.game or self.dlc):
            raise forms.ValidationError('Game or DLC must be provided.')
        return clean_data
        
    def save(self, commit=True):
        rating = super().save(commit=False)
        
        if self.user:
            rating.user = self.user
        if self.game:
            rating.game = self.game
        if self.dlc:
            rating.dlc = self.dlc
        if self.comment:
            rating.comment = self.comment
            
        if commit:
            rating.save()
            
        return rating
            
        