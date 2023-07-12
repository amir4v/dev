from copy import copy

from django.shortcuts import render, redirect
from django.conf import settings
from django import forms
from django.http import HttpResponse

from .models import Post
from .forms import PostModelForm

_BASE_DIR = settings.BASE_DIR

from middlevel.tasks import do_send_mail
def send_mail_to(request, subject, message, to):
    do_send_mail.delay(subject, message, to)
    return HttpResponse('Sent.')




def login(request):
    print(request.GET)
    print(request.POST)
    print(request.FILES)
    return render(request, 'login.html')




def upload(request):
    # Post.objects.using('postgres').create(title='test-title')
    # open(settings.BASE_DIR / 'postgres.log', 'a').write(
    #     str(Post.objects.using('postgres').count())+'\n'+str(Post.objects.using('postgres').last())+'\n'
    # )
    
    # Post.objects.using('mysql').create(title='test-title')
    # open(settings.BASE_DIR / 'mysql.log', 'a').write(
    #     str(Post.objects.using('mysql').count())+'\n'+str(Post.objects.using('mysql').last())+'\n'
    # )
    
    """
    import pymongo
    client = pymongo.MongoClient('mongodb://mongodb:27017/default_mongo')
    #Define DB Name
    dbname = client['default_mongo']
    #Define Collection
    collection = dbname['default_mongo']
    mascot_1={
        "name": "Sammy",
        "type" : "Shark"
    }
    collection.insert_one(mascot_1)
    mascot_details = collection.find({})
    for r in mascot_details:
        print(r['name'])
    """
    
    form = PostModelForm()
    if request.method == 'GET':
        return render(request, 'app/upload.html', {'form': form})
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = PostModelForm()
            return render(request, 'app/upload.html', {'form': form})
        return render(request, 'app/upload.html', {'form': form})


class UploadForm(forms.Form):
    file = forms.FileField()


def upload_file(request):
    print('1.-')
    if request.method == "POST":
        print('2.-')
        handle_uploaded_file(request.FILES["file"])
        print('3.-')
        return redirect("/upload_file")
    print('4.-')
    return render(request, "app/upload.html", {'form': UploadForm(), 'path': 'upload_file'})


def handle_uploaded_file(f):
    print('5.-')
    with open(_BASE_DIR / "media/file_name", "wb+") as destination:
        for chunk in f.chunks():
            print('6.-')
            destination.write(chunk)