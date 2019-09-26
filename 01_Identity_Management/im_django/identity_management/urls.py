from django.urls import path
from . import views

# Register app name
app_name = 'identity_management'

# Create urls here
urlpatterns = [
    #path('', views.homepage, name='home'),  # map home view
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<int:id>/', views.activate, name='activate'),
    path('auth_login/', views.auth_login.as_view(), name='auth_login'),
    path('users/', views.ListUsers.as_view(), name='users'),
]