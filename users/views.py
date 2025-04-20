from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ForgotPasswordForm
from users.firebase_helpers import firebase_config
from django.contrib import messages
# from users.firebase_helpers import firebase_config

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            request.session['uid'] = str(user['idToken'])
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'errors': form.errors})


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
    return render(request, 'users/signup.html', {'form': form, 'errors': form.errors})


def profile(request):
    return render(request, 'users/profile.html')


def logout_view(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
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