"""
URL configuration for DriveStorage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drive.views import signup, loginUser, index, logoutUser, upload_files, delete_file, change_path, go_back, new_folder, delete_folder
from drive.views import download_as_zip, download_file
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('upload', upload_files, name='upload_file'),
    path('signup', signup, name='signup'),
    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout'),
    path('deleteFile/<int:file_id>', delete_file, name='delete'),
    path('change/<str:filepath>', change_path, name='change_dir'),
    path('back', go_back, name='go_back'),
    path('new_folder', new_folder, name='new_folder'),
    path('delete_folder/<str:folder>', delete_folder, name='delete_folder'),
    path('download_as_zip/<str:folder>', download_as_zip, name="download_as_zip"),
    path('download<path:file_path>', download_file, name="download_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
