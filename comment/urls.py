from django.urls import path
from . import views

urlpatterns = [
    path('create-comment/<int:post_id>/', views.comment_view, name='create-comment'),
    path('delete-comment/<int:post_comment_id>/', views.delete_comment, name='delete-comment'),
    path('set-comment/<int:post_comment_id>/', views.set_comment, name='set-comment'),
]
