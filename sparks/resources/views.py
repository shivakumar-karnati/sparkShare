from django.shortcuts import render,redirect ,get_object_or_404
from django.conf import settings
# from sparks.sparks import settings
from .models import resources_post,profile
from .forms import uploadform , blogpost,RegisterForm
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
    docs = resources_post.objects.all()

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


@login_required
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

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # 🔹 Generate UID + Token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # 🔹 Create activation link
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={
                    'uidb64': uid,
                    'token': token
                })
            )

            # 🔹 Send Email with link
            send_mail(
                "Activate Your Account",
                f"Click the link below to activate your account:\n\n{activation_link}",
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            messages.success(request, "Activation link sent to your email 📧")
            return redirect("user_login")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("user_login")
    else:
        return redirect("register")


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






    


