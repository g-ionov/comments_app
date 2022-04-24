from django.contrib import admin
from django.urls import path, include
from blog import settings
from blog.yasg import urlpatterns as yasg_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('comments.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
                  ] + urlpatterns
    urlpatterns += yasg_urls
