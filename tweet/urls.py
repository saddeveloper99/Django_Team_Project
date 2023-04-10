from django.urls import path
from . import views
urlpatterns = [
    path('create-post/', views.create_post,),
    path('', views.home, name='홈페이지'),
]
