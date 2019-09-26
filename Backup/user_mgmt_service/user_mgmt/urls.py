from django.urls import path
from . import views

# Register app name
app_name = 'user_mgmt'

# Create urls here
urlpatterns = [
    #path('', views.homepage, name='home'),  # map home view
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<int:id>/', views.activate, name='activate'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/logout/', views.Logout.as_view(), name='logout'),
]