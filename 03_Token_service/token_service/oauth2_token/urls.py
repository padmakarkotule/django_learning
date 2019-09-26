from django.urls import path, re_path
from . import views

# Register app name
app_name = 'oauth2_token'

urlpatterns = [
    #path('', views.homepage, name='home'),  # map home view
    path('oauth/get_token', views.GetToken.as_view(), name='signup'),
    path('oauth/verify_token/', views.VerifyToken.as_view(), name='login'),
]