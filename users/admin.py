from django.contrib import admin
from users.models import MyUser
from django.contrib.auth.admin import UserAdmin
from users.firebase_helpers import firebase_config
from django.contrib import messages

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('created_at',)
    actions = ['reset_password']

    def reset_password(self, request, queryset):
        firebase = firebase_config()
        auth = firebase.auth()
        success_count = 0
        for user in queryset:
            try:
                auth.send_password_reset_email(user.email)
                success_count += 1
                print(f"Password reset email sent to: {user.email}")
            except Exception as e:
                error_msg = str(e)
                print(f"Firebase reset password error for {user.email}: {error_msg}")
                self.message_user(request, f"Failed to send reset email to {user.email}: {error_msg}", level=messages.ERROR)
        if success_count > 0:
            self.message_user(request, f"Password reset emails sent to {success_count} user(s).", level=messages.SUCCESS)

    reset_password.short_description = "Send password reset email"


admin.site.register(MyUser, CustomUserAdmin)
