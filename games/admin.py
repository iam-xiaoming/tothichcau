from django.contrib import admin
from .models import Game, Key, UserGame, GameHero, Category, Comment
from django import forms
from django.forms import CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from cart.models import Transaction

# Register your models here.
admin.site.register(GameHero)
admin.site.register(Category)


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
    
    
@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['game']
    list_display = ('key', 'game', 'status',)
    list_filter = ('status', 'game__name')
    search_fields = ('key', 'game__name')


@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'key', 'key_status', 'created_at',)
    list_filter = ('game',)
    search_fields = ('user__email', 'user__username', 'game__name')
    autocomplete_fields = ('user', 'game')
    
    def key_status(self, obj):
        return obj.key.status
    
    def created_at(self, obj):
        return Transaction.objects.get(user=obj.user, game=obj.game).created_at
    
    key_status.short_description = 'key status'
    created_at.short_description = 'created at'
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'title', 'created_at',)
    list_filter = ('user', 'game',)
    search_fields = ('user', 'game',)
    autocomplete_fields = ('user', 'game',)
