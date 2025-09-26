from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.cache import never_cache

from .utils import send_otp_email  

User = get_user_model()


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_email_verified:
                login(request, user)
                return redirect('task_list')
            else:
                messages.error(request, "Please verify your email before logging in.", extra_tags="login")
                return redirect('login')
        messages.error(request, "Invalid login credentials", extra_tags="login")
        return redirect('login')

    return render(request, 'login.html')


@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.", extra_tags="register")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists." , extra_tags="register")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        send_otp_email(user)
        request.session['user_email'] = email
        return redirect('verify_otp')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def verify_otp_view(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        email = request.session.get("user_email")
        try:
            user = User.objects.get(email=email)
            if user.otp_code == otp_input and timezone.now() < user.otp_expiry:
                user.is_email_verified = True
                user.otp_code = ''
                user.save()
                login(request, user)
                return redirect('task_list')

            else:
                messages.error(request, "Invalid or expired OTP." , extra_tags="verify_otp")
                return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('register')

    return render(request, 'verify_otp.html')



def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            send_otp_email(user)
            request.session['reset_email'] = email
            messages.success(request, "We sent you an OTP to reset your password.",extra_tags="forgot_password")
            return redirect('reset_password_verify')
        except User.DoesNotExist:
            messages.error(request, "No account with that email.", extra_tags="forgot_password")
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def reset_password_verify_view(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        email = request.session.get("reset_email")

        try:
            user = User.objects.get(email=email)
            if user.otp_code == otp_input and timezone.now() < user.otp_expiry:
                user.otp_code = ''
                user.save()
                request.session['reset_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired OTP.",extra_tags="reset_password_verify")
                return redirect('reset_password_verify')

        except User.DoesNotExist:
            messages.error(request, "User not found.", extra_tags="reset_password_verify")
            return redirect('forgot_password')

    return render(request, 'reset_password_verify.html')



def reset_password_view(request):
    if not request.session.get('reset_verified'):
        messages.error(request, "You must verify OTP first.", extra_tags="reset_password")
        return redirect('forgot_password')

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.session.get("reset_email")

        if password1 != password2:
            messages.error(request, "Passwords do not match.", extra_tags="reset_password")
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()

            
            request.session.pop('reset_email', None)
            request.session.pop('reset_verified', None)

            
            login(request, user)
            return redirect('task_list')  

        except User.DoesNotExist:
            messages.error(request, "User not found.", extra_tags="reset_password")
            return redirect('forgot_password')

    return render(request, 'reset_password.html')

