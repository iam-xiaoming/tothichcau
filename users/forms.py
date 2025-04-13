from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
import re
from users.utils import *

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))
    
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid email or password.')
        
        self.user = user
        
        return super().clean()
    
    
    def get_user(self):
        return self.user
    
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput({
        'placeholder': 'Email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput({
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput({
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        
    

    def save(self, commit=True):
        firebase_config()

        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        display_name = email.split('@')[0]  # hoặc cho người dùng nhập tên

        # 1. Tạo user trên Firebase Authentication
        try:
            user_record = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )

            # 2. Gán custom claims mặc định (ví dụ: role='user')
            auth.set_custom_user_claims(user_record.uid, {'role': 'user'})

        except Exception as e:
            print(f"Firebase error: {e}")
            raise forms.ValidationError("Không thể tạo tài khoản Firebase.")

        # 3. Lưu vào local database (Django)
        user = super().save(commit=False)
        user.username = display_name
        user.email = email
        user.id = user_record.uid  # nếu model có field này
        user.set_password(password)

        if commit:
            user.save()

        return user
    