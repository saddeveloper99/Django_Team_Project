from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweet.urls')),  # tweet app urls 연결
    path('', include('user.urls')),  # user app urls 연결
    path('', include('comment.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)