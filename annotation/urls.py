from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create_leader/', LeaderCreateView.as_view(), name='leader_create'),
    path('batch_upload/', BatchUploadView.as_view(), name='batch_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
