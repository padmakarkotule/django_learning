"""im_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('identity_management.urls', namespace='identity_management'), ),

    # accounts login
    #path('accounts/login/', views.LoginView.as_view(), name='login'),
    ### path('accounts/profile/', views.TemplateView.as_view(template_name='ui/home/profile.html'), name='profile'),
    #path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    # Password reset
    #path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    #path('accounts/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Password reset confirm
    # path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password change
    # path('accounts/password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('accounts/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
