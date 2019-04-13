from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from keeperapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('user/sign-in', auth_views.LoginView.as_view(template_name='user/sign_in.html'),
        name='user-sign-in'),
    path('user/sign-out', auth_views.LogoutView.as_view(next_page='/'),
        {'next-page': ''},
        name='user-sign-out'),
    path('user/', views.user_home, name='user-home')
]
