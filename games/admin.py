from django.contrib import admin
from .models import Game
from keys.models import Key
from game_features.models import Category
from django import forms
from django.forms import CheckboxSelectMultiple
from django.core.exceptions import ValidationError

# Register your models here.
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
    
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'price', 'discount', 'quantity', 'category_list', 'release_date')
    list_filter = ('publisher', 'categories', 'release_date')
    search_fields = ('name', 'publisher', 'categories__name')
    ordering = ('-release_date',)
    form = GameAdminForm
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    
    
    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if categories and categories.count() > 4:
            raise ValidationError("Cannot select more than 4 categories.")
        return categories
    
    
