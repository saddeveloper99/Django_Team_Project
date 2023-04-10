from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.create_post, name='create-post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete-post'),
    path('set-post/<int:post_id>/', views.set_post, name='set-post'),
]
