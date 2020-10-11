from django.contrib import admin
from django.urls import path
import ckeditorapp.views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ckeditorapp.views.index, name='index'),
    path('blogMain/', ckeditorapp.views.blogMain, name='blogMain'),
    path('blogMain/createBlog/', ckeditorapp.views.createBlog, name='createBlog'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
