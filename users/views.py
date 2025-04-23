from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ForgotPasswordForm, UserUpdateForm
from users.firebase_helpers import firebase_config
from django.contrib import messages
from games.models import UserGame
# from users.firebase_helpers import firebase_config
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.views.generic.edit import FormMixin
from games.models import Category

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            user_instance = form.get_user_instance()
            
            login(request, user_instance)
            
            request.session['uid'] = str(user['idToken'])
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
        
    context = {
        'form': form,
        'errors': form.errors,
        'categories': Category.objects.all()
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # # Đăng nhập tự động sau khi đăng ký (tùy chọn)
            # firebase = firebase_config()
            # auth = firebase.auth()
            # user_record = auth.sign_in_with_email_and_password(
            #     form.cleaned_data['email'],
            #     form.cleaned_data['password1']
            # )
            # request.session['uid'] = user_record['localId']
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm() 
        
    context = {
        'form': form,
        'errors': form.errors,
        'categories': Category.objects.all()
    }
    return render(request, 'users/signup.html', context)


class ProfileView(LoginRequiredMixin, FormMixin, ListView):
    model = UserGame
    template_name = 'users/profile.html'
    context_object_name = 'user_games'
    login_url = 'login'
    ordering = ['-transaction__created_at']
    paginate_by = 10
    form_class = UserUpdateForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
        
    
    def get_queryset(self):
        return UserGame.objects.filter(user=self.request.user)
    
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path


def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'users/home.html')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            firebase = firebase_config()
            auth = firebase.auth()

            try:
                # Gửi email đặt lại mật khẩu
                auth.send_password_reset_email(email)
                print(f"Password reset email sent to: {email}")
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('forgot_password')  # Hoặc chuyển hướng đến trang khác
            except Exception as e:
                error_msg = str(e)
                print(f"Firebase reset password error: {error_msg}")
                if "EMAIL_NOT_FOUND" in error_msg:
                    messages.error(request, "No account found with this email address.")
                elif "INVALID_EMAIL" in error_msg:
                    messages.error(request, "Invalid email address.")
                else:
                    messages.error(request, f"Failed to send reset email: {error_msg}")
                return render(request, 'users/forgot_password.html', {'form': form})
        else:
            print(form.errors)
    else:
        form = ForgotPasswordForm()

    return render(request, 'users/forgot_password.html', {'form': form})