from django.urls import path, re_path
from . import views

# Register app name
app_name = 'jwt_token'

# Create urls here
urlpatterns = [
    #path('', views.homepage, name='home'),  # map home view
    path('jwt/get_token/', views.GetToken.as_view(), name='signup'),
    path('jwt/verify_token/', views.VerifyToken.as_view(), name='login'),
]