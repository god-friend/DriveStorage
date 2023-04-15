from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUp, LoginForm, UploadForm
from .models import User, UploadedFiles
from django.contrib.auth import authenticate, login, logout
from .extras import get_folders, create_dir, file_exists, remove_folder, create_archive
import mimetypes, os
from django.conf import settings

CURRENT_PATH = {}
MESSAGE = ''
ERROR = ''

def add_key(key):
    global CURRENT_PATH
    CURRENT_PATH[key] = "/"

def change_msgError(message, Error):
    global MESSAGE, ERROR
    MESSAGE = message
    ERROR = Error

def validate_request(request, method):
    if request.method == method and str(request.user) != "AnonymousUser":
        return True
    return False

def signup(request):
    
    form = None
    if request.method == 'POST':
        form = SignUp(request.POST)

        if form.is_valid():
            un = form.cleaned_data['username']
            fn = form.cleaned_data['firstname']
            ln = form.cleaned_data['lastname']
            em = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd']
            User.objects.create_user(username=un, first_name=fn, last_name=ln, email=em, password=pwd)

            return redirect('/login')
       
    if request.method == 'GET':
        form = SignUp(label_suffix=" :: ")
        return render(request, 'signup.html', context={"form": form}) 
    return render(request, 'signup.html', context={"form": form})

def loginUser(request):
    form = None
    error_login = None
    if request.method == 'GET':
        form = LoginForm(label_suffix=" :: ")
        return render(request, 'login.html', context={"form": form, "error_login": error_login})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd']
            user = authenticate(username=un, password=pwd)
            if not user:
                error_login = "Username and Password Doesn't Match"
            else:
                login(request, user)
                add_key(user)
                return redirect('/')
    return render(request, 'login.html', context={"form": form, "error_login": error_login})

def logoutUser(request):
    logout(request)
    return redirect('/')

def index(request):
    global CURRENT_PATH
    data = {}
    if validate_request(request, "GET"):
        files = UploadedFiles.objects.filter(user=request.user, path=CURRENT_PATH[request.user])
        data["files"] = files
        data["folders"] = get_folders(request.user, CURRENT_PATH[request.user])
        data["current_path"] = CURRENT_PATH[request.user]
        data["form"] = UploadForm(label_suffix=" :: ")
        data["message"] = MESSAGE
        data["error"] = ERROR
        return render(request, 'myfiles.html', context=data)
    return render(request, 'myfiles.html')
    
def upload_files(request):

    if validate_request(request, "POST"):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            all_files = request.FILES.getlist('file')
            for files in all_files:
                if file_exists(request.user, CURRENT_PATH[request.user], files.name):
                    change_msgError("", str(files.name) + " Already Exists")
                    return redirect('/')
                file_obj = UploadedFiles.objects.create(user=request.user, path=CURRENT_PATH[request.user], file=files)
                file_obj.link = request.build_absolute_uri("download/"+file_obj.file.url)
                file_obj.save()
            
            if len(all_files) >= 1:
                change_msgError("Successfully Uploaded " + str(len(all_files)) + " files", "")
            else:
                change_msgError("", "No File Provided")
            return redirect('/')
        
    return HttpResponse("Method Not Allowed")

def delete_file(request, file_id):
    filename = ""
    if validate_request(request, "GET"):
        file = UploadedFiles.objects.get(id=file_id)
        filename = file.filename()
        file.delete()

    change_msgError("Successfully Deleted "+filename, "")
    return redirect('/')

def go_back(request):
    global CURRENT_PATH
    if validate_request(request, "GET"):
        if CURRENT_PATH[request.user] != '/' and len(CURRENT_PATH) > 1:
            if CURRENT_PATH[request.user].endswith('/'):
                CURRENT_PATH[request.user] = CURRENT_PATH[request.user][:-1]
            p = CURRENT_PATH[request.user].split('/')
            p.pop()
            if len(p) == 1:
                CURRENT_PATH[request.user] = "/"
            else:
                CURRENT_PATH[request.user] = "/".join(p) + "/"
        change_msgError("", "")
        return redirect('/')
    return HttpResponse("Method Not Allowed")

def change_path(request, filepath):
    global CURRENT_PATH
    if validate_request(request, "GET"):
        change_msgError("", "")
        CURRENT_PATH[request.user] += filepath + '/'
        return redirect('/')
    return HttpResponse("Method Not Allowed")

def new_folder(request):
    global MESSAGE
    if validate_request(request, "POST"):
        if create_dir(request.user, CURRENT_PATH[request.user], request.POST['newF']):
            change_msgError(request.POST["newF"] + " Created Successfully", "")
        else:
            change_msgError("", request.POST["newF"]+" Already Exists")
        return redirect('/')
    
    return HttpResponse("Method Not Allowed")

def delete_folder(request, folder):
    if validate_request(request, "GET"):
        if remove_folder(request.user, CURRENT_PATH[request.user], folder):
            change_msgError(folder+" Deleted Successfully", "")
        else:
            change_msgError("", "Unable to Delete "+folder)

        return redirect('/')
    return HttpResponse("Method Not Allowed")

def download_as_zip(request, folder):
    if validate_request(request, "GET"):
        archive = None
        try:
            archive = create_archive(request.user, CURRENT_PATH[request.user], folder)
            path = open(archive, 'rb')
            mimetype, _ = mimetypes.guess_type(archive)
            response = HttpResponse(path, content_type=mimetype)
            response["Content-Disposition"] = "attachement: filname=%s.zip"%folder
            return response
        finally:
            if archive is not None:
                os.remove(archive)
    return HttpResponse("Method Not Allowed")

def download_file(request, file_path):

    if request.method == "GET":
        file_path = file_path.replace('/media', "")
        file_path = settings.MEDIA_ROOT + file_path
        file = open(file_path, 'rb')
        response = HttpResponse(file, content_type="application/force-download")
        response['Content-Disposition'] = "attachment: filename=%s"%file.name
        
        return response
    
    return HttpResponse("Method Not Allowed")
