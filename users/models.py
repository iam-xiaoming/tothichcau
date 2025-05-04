from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from users.firebase_helpers import firebase_config
import time
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, role='user', **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        
        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Tạo user trên Firebase Authentication
        firebase = firebase_config()
        auth = firebase.auth()
        db = firebase.database()

        try:
            user_record = auth.create_user_with_email_and_password(
                email=email,
                password=password
            )
            print(f"Superuser created in Firebase: {user_record}")
        except Exception as e:
            error_msg = str(e)
            print(f"Firebase auth error: {error_msg}")
            if "EMAIL_EXISTS" in error_msg:
                raise ValueError("This email is already registered in Firebase.")
            elif "INVALID_EMAIL" in error_msg:
                raise ValueError("Invalid email address.")
            elif "WEAK_PASSWORD" in error_msg:
                raise ValueError("Password is too weak.")
            else:
                raise ValueError(f"Unable to create Firebase account: {error_msg}")

        # Lưu thông tin vào Realtime Database
        uid = user_record['localId']
        username = extra_fields.get('username', email.split('@')[0][:20])
        user_data = {
            'email': email,
            'username': username,
            'role': 'admin',
            'created_at': int(time.time()),
            'is_active': True,
            'is_staff': True,
            'is_superuser': True
        }
        try:
            db.child("users").child(uid).set(user_data, user_record['idToken'])
            print(f"Superuser data saved to Realtime Database for UID: {uid}")
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise ValueError(f"Unable to save superuser data to database: {str(e)}")

        # Tạo user trong Django
        user = self.model(
            id=uid,
            email=email,
            username=username,
            role='admin',
            created_at=timezone.now(),
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
class MyUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    id = models.CharField(max_length=50, primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='users/donate.jpg', upload_to='users/')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    def __str__(self):
        return self.email



class UserGame(models.Model):    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_games')
    
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_owned_by_users', null=True, blank=True, editable=False)
    dlc = models.ForeignKey('games.DLC', on_delete=models.CASCADE, related_name='dlc_owned_by_users', null=True, blank=True, editable=False)
    
    key = models.ForeignKey('keys.Key', on_delete=models.CASCADE, related_name='user_game')
    transaction = models.ForeignKey('cart.Transaction', on_delete=models.CASCADE, related_name='user_game')
    
    def __str__(self):
        if self.game:
            return f"{self.user.email} owns {self.game.name}"
        
        return f"{self.user.email} owns {self.dlc.name}"
    
    def clean(self):
        super().clean()
        
        if not (self.game or self.dlc):
            raise ValidationError('Game or DLC must be not none.')


# comment
class Comment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='comment', null=True, blank=True, editable=False)
    dlc = models.ForeignKey('games.DLC', on_delete=models.CASCADE, related_name='comment', null=True, blank=True, editable=False)
    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title