import os
from django.conf import settings
from shutil import rmtree, make_archive
from .models import UploadedFiles

MEDIA_DIR = settings.MEDIA_ROOT


def upload_files(file, user):
    with open('media/'+str(user)+'/'+file.name, 'wb+') as dest:
        for chunks in file.chunks():
            dest.write(chunks)
    dest.close()
    return True


def create_dir(user, path, dir_name):
    new_folder = MEDIA_DIR+'/'+str(user)+path+dir_name
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        return True
    return False

def get_folders(user, path):
    folders = []
    for f in os.listdir(MEDIA_DIR+'/'+str(user)+path):
        if os.path.isdir(os.path.join(MEDIA_DIR+'/'+str(user)+path, f)):
            folders.append(f)
    return folders

def file_exists(user, path, filename):
    if os.path.exists(MEDIA_DIR+'/'+str(user)+path+filename):
        return True
    return False

def folder_exists(user, path, dir_name):
    if os.path.exists(MEDIA_DIR+'/'+str(user)+path+dir_name):
        return True
    return False

def remove_folder(user, path_dir, folder_name):

    if folder_exists(user, path_dir, folder_name):
        files = UploadedFiles.objects.filter(user=user, path__startswith=path_dir+folder_name)
        for file in files:
            file.delete()
        
        rmtree(MEDIA_DIR+'/'+str(user)+path_dir+folder_name)

    return True

def create_archive(user, path, dir_name):

    if not os.path.exists(MEDIA_DIR+'/temp'):
        os.mkdir(MEDIA_DIR+"/temp")

    archive = make_archive(MEDIA_DIR+'/temp/'+dir_name, "zip", MEDIA_DIR+'/'+str(user)+path+dir_name)
    return archive