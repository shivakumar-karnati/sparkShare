"""
URL configuration for sparks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resources import views

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.basepage,name="basepage"),
    path('home/', views.homepage,name="homepage"),
    path('resources/', views.resources_view,name="resource_view"),
    path('edit_post/<int:id>/', views.edit_post,name="edit_post"),
    path('delete_post/<int:id>/', views.delete_post,name="delete_post"),
    path('upload/',views.resource_upload,name="upload"),
    path('register/',views.register,name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('login/',views.user_login,name="user_login"),
    path('logout/',views.user_logout,name="user_logout"),
    path('password_change/',views.change_password,name="password_change"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),


   path('activate/<uidb64>/<token>/', views.activate, name='activate'), 


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

