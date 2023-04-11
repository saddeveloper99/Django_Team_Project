
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweet.urls')),  # tweet app urls 연결
    path('', include('user.urls')),  # user app urls 연결
]
