from django.contrib import admin
from .models import Order, Transaction
from django.contrib import admin

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_object_name', 'get_type', 'key', 'get_object_price', 'get_object_discount_price', 'created_at',)
    
    def get_object_name(self, obj):
        if obj.game:
            return obj.game.name
        return obj.dlc.name
    
    def get_type(self, obj):
        if obj.game:
            return 'Base Game'
        return 'Downloadable Content'
    
    def get_object_price(self, obj):
        if obj.game:
            return obj.game.price
        return obj.dlc.price
    
    def get_object_discount_price(self, obj):
        if obj.game:
            return obj.game.discounted_price
        return obj.dlc.discounted_price
        
    
    get_type.short_description = 'type'
    get_object_name.short_description = 'game'
    get_object_price.short_description = 'price'
    get_object_discount_price.short_description = 'discount_price'
    


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'get_user_key_game', 'status', 'total_amount', 'created_at')
    
    def get_user_key_game(self, obj):
        return obj.key
    
    get_user_key_game.short_description = 'key'