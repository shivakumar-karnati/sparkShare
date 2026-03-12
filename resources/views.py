from django.shortcuts import render,redirect ,get_object_or_404
from django.conf import settings
# from sparks.sparks import settings
from .models import resources_post,profile
from .forms import uploadform , RegisterForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required , permission_required
# from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def basepage(request):
    return render(request, "base.html")

# @login_required
def homepage(request):

    if request.user.is_authenticated:
        template = "home.html"
    else:
        template = "base.html"

    return render(request, template)


def resources_view(request):
    docs = resources_post.objects.all().order_by('-id')

    action = request.GET.get("action")
    file_id = request.GET.get("id")

    if action and file_id:
        doc = get_object_or_404(resources_post, id=file_id)

        # 🔐 Require login for both view & download
        if not request.user.is_authenticated:
            messages.error(request, "You must login to access this resource ❌")
            return redirect("resource_view")

        return redirect(doc.file.url)

    return render(request, "resources_view.html", {"docs": docs})


from django.http import FileResponse
from django.shortcuts import get_object_or_404

import os

@login_required
def download_pdf(request, pk):
    doc = get_object_or_404(resources_post, id=pk)

    file_path = doc.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


# @permission_required("resources.change_resources_post",raise_exception=True)
@login_required
def edit_post(request, id):
    post = get_object_or_404(resources_post,id=id)

    # 🔐 Security check: only owner can edit
    # if post.user != request.user:
    #     return redirect("profile")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.subject = request.POST.get("subject")
        # post.content = request.POST.get("content")

        if request.FILES.get("file"):
            post.file = request.FILES.get("file")

        post.save()
        return redirect("profile")

    return render(request, "edit_post.html", {"post": post})

@login_required
def delete_post(request,id):
    post = get_object_or_404(resources_post,id=id)
    if request.method == "POST":
        post.delete()
        return redirect("profile")
    return render(request,"delete_post.html",{"post":post})

def resource_upload(request):

    if request.method == "POST":
        form = uploadform(request.POST, request.FILES)

        # 🔐 Check login when submitting
        if not request.user.is_authenticated:
            messages.error(request, "You must login to upload a resource ❌")
            return render(request, "upload.html", {"form": form})

        # ✅ If logged in, validate form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Resource uploaded successfully ✅")
            return redirect("upload")

        else:
            messages.error(request, "Please fix the errors below ❌")

    else:
        form = uploadform()

    return render(request, "upload.html", {"form": form})


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages

import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            otp = random.randint(100000,999999)

            request.session['register_data'] = form.cleaned_data
            request.session['otp'] = otp
            request.session['otp_time'] = time.time()

            email = form.cleaned_data['email']

            try:
                send_mail(
                    "OTP Verification",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )
            except Exception as e:
                print("Email Error:", e)

            return redirect("verify_otp")

    else:
        form = RegisterForm()

    return render(request,"register.html",{"form":form})
from django.contrib.auth.models import User
import time
def verify_otp(request):

    if "register_data" not in request.session:
        return redirect("register")

    if request.method == "POST":

        user_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        otp_time = request.session.get("otp_time")

        # 10 minute expiry
        if time.time() - otp_time > 600:
            messages.error(request,"OTP expired")
            return redirect("register")

        if str(real_otp) == str(user_otp):

            data = request.session.get("register_data")

            from django.contrib.auth.models import User

            User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password1"]
            )

            del request.session["register_data"]
            del request.session["otp"]
            del request.session["otp_time"]

            messages.success(request,"Account created successfully")
            return redirect("user_login")

        else:
            messages.error(request,"Invalid OTP")

    return render(request,"verify_otp.html")

import random

def resend_otp(request):

    if "register_data" not in request.session:
        return redirect("register")

    otp = random.randint(100000,999999)

    request.session["otp"] = otp
    request.session["otp_time"] = time.time()

    email = request.session["register_data"]["email"]

    send_mail(
        "New OTP Code",
        f"Your new OTP is {otp}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

    messages.success(request,"OTP resent")

    return redirect("verify_otp")

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request , data = request.POST)
        # if not user.is_active:
        #     messages.error(request, "Please verify your email first 📧")
        #     return redirect("user_login")
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password ❌")
        
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{"form":form})


@login_required
def profile_view(request):
    user_posts = resources_post.objects.filter(author=request.user)
    return render(request, "profile.html" , {"user_posts": user_posts})



def user_logout(request):
    logout(request)
    return redirect("basepage")

@login_required
def change_password(request):
    if request.method  == "POST":
        form = PasswordChangeForm(user = request.user , data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request , user)
            messages.success(request, "passsword change successfully")
            return redirect("homepage")
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, "change_password.html",{"form":form})






    


