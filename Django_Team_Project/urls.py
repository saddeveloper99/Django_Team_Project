
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/',include('tweet.urls')), # tweet app urls 연결
]
