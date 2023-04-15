from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-post/', views.create_post, name='create-post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete-post'),
    path('set-post/<int:post_id>/', views.set_post, name='set-post'),
    path('', views.home, name='홈페이지'),
    path('my-page/<int:user_id>/', views.my_page, name='my-page'),
    path('set-profile/<int:user_id>/', views.set_profile, name='set-profile'),
    path('post-detail/<int:post_id>/', views.post_detail, name='post-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
