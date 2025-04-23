from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.firebase_helpers import firebase_config
from users.models import MyUser
from django.utils import timezone
import traceback
import time
from django.shortcuts import get_object_or_404


User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'class': 'form-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-input'
    }))
    
    def clean(self):
        firebase = firebase_config()
        auth = firebase.auth()

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        if not email or not password:
            raise forms.ValidationError("Email and password are required.")
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_instance = get_object_or_404(MyUser, email=email)
        except Exception as e:
            print(f"Firebase auth error: {str(e)}")
            raise forms.ValidationError("Invalid email or password.")
        
        self.user = user
        self.user_instance = user_instance
        return self.cleaned_data
    
    def get_user(self):
        return self.user
    
    def get_user_instance(self):
        return self.user_instance
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput({
        'placeholder': 'Email address',
        'class': 'form-input'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput({
        'placeholder': 'Password',
        'class': 'form-input'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput({
        'placeholder': 'Confirm Password',
        'class': 'form-input'
    }))
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')

        # Kiểm tra mật khẩu
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        if len(password1) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")

        # Kiểm tra username mặc định
        username = email.split('@')[0][:20]
        print(f"Generated username: {username}")
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This email generates a username that is already taken.")

        return cleaned_data

    def save(self, commit=True):
        firebase = firebase_config()
        authe = firebase.auth()
        db = firebase.database()

        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        display_name = email.split('@')[0]  # hoặc cho người dùng nhập tên

        # 1. Tạo user trên Firebase Authentication
        try:
            user_record = authe.create_user_with_email_and_password(
                email=email,
                password=password
            )
        except Exception as e:
            error_msg = str(e)
            print(f"Firebase auth error: {error_msg}")
            traceback.print_exc()
            # Xử lý các lỗi cụ thể từ Firebase
            if "EMAIL_EXISTS" in error_msg:
                raise forms.ValidationError("This email is already registered.")
            elif "INVALID_EMAIL" in error_msg:
                raise forms.ValidationError("Invalid email address.")
            elif "WEAK_PASSWORD" in error_msg:
                raise forms.ValidationError("Password is too weak.")
            else:
                raise forms.ValidationError(f"Unable to create Firebase account: {error_msg}")
        
        uid = user_record['localId']
        # 2. Lưu thông tin người dùng vào Firebase Realtime Database
        user_data = {
            'email': email,
            'username': display_name,
            'role': 'user',
            'created_at': int(time.time()),
            'is_active': True,
            'is_staff': False
        }
        try:
            db.child("users").child(uid).set(user_data, user_record['idToken'])
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise forms.ValidationError("Unable to save user data to database.")
        
        # 3. Lưu vào local database (Django)
        user = MyUser(
            id=uid,  # Gán uid vào trường id
            email=email,
            username=display_name,
            role='user',
            created_at=timezone.now(),
        )
        if commit:
            try:
                user.save()
            except Exception as e:
                print(f"Django save error: {str(e)}")
                raise forms.ValidationError("Unable to save user to Django database.")

        return user
    

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'readonly': 'readonly'
    }))
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'full_name']