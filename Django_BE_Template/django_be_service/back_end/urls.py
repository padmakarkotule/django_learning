from django.urls import path, re_path
from . import views

# Register app name
app_name = 'back_end'

# Create urls here
urlpatterns = [
    #path('', views.homepage, name='home'),  # map home view
    path('be/create/', views.Create_post.as_view(), name='create'),
    path('be/list/', views.List_get.as_view(), name='create'),
]