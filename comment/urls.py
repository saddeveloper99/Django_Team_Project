from django.urls import path
from . import views

urlpatterns = [
    path('comment-view/',views.comment_view,name='comment-view')
]
