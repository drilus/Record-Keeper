from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from keeperapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='user_main'),
    path('user/', views.user_home, name='user-home'),
    path('user/sign-in', auth_views.LoginView.as_view(template_name='user/sign_in.html'),
         name='user-sign-in'),
    path('user/sign-out', auth_views.LogoutView.as_view(next_page='/'),
         {'next-page': ''},
         name='user-sign-out'),
    path('user/sign-up', views.user_sign_up, name='user-sign-up'),
    path('user/overview', views.user_overview, name='user-overview'),
    path('user/settings', views.user_settings, name='user-settings'),
    path('user/categories', views.user_categories, name='user-categories'),
    path('user/edit_category/<int:category_id>/', views.edit_category, name='edit-category'),
    path('user/add_category', views.add_category, name='add-category'),
    path('user/records', views.user_records, name='user-records'),
    path('user/record_info/<int:category_id>/', views.user_record_info, name='user-records'),
    path('user/edit_record/<int:record_id>/', views.edit_record, name='edit-record'),
    path('user/add_record', views.add_record, name='add-record'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
