# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from project.models import *
from .forms import *
import os
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User




def index(request):
    return render(request, 'project/index.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        this_user = authenticate(request, username=username, password=password)
        if this_user is not None:
            login(request, this_user)
            print(request.user)
            return redirect(course_list)
            # return render(request, 'project/index.html', {'error_message': "Incorrect Username or Password."})
        # for users in user.objects.all():
        #     if username == users.user_name and password == users.password:
        #         return redirect(course_list)
        else:
            return render(request, 'project/index.html', {'error_message': "Please Log In."})
    return render(request, 'project/index.html')

def register(request):
    return render(request, 'project/register.html')


def check_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username,
                            password=password,
                            email=email)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return redirect(index)


@login_required
def course_list(request):

    ##if not user redirect to index w/ message need to sign in
    courses = course.objects.all()
    for course_ in courses: print(course_)
    user = request.user
    return render(request, 'project/dashboard.html', {'courses': courses})

@login_required
def course_view(request, identity):

    if request.method == "POST":
        course_name = request.POST.get("course_name")
        files = file.objects.filter(course=course.objects.get(course_name=course_name))
        user = request.user
        return render(request, 'project/class_view.html', {'files': files,
                                                           'course_name': course_name})
@login_required
def file_upload(request):
    this_user = request.user

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            fileuploading = form.save(commit=False)
            fileuploading.username = request.user
            fileuploading.save()
            courses = course.objects.all()
            return render(request, 'project/dashboard.html', {'courses': courses})
    else:
        form = FileForm()
        return render(request, 'project/file_upload.html', {'form': form})


@login_required
def download(request, file_chosen):
    if not request.user.is_authenticated:
        return redirect(index)
    file_path = settings.MEDIA_ROOT + '/' + file_chosen
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            file_object = file.objects.get(file_link=file_chosen)
            file_downloaded = downloaded_file.objects.create(file_downloaded=file_object, username=request.user)
            file_downloaded.save()
            print(file_downloaded.file_downloaded)
            print(request.user)
            return response
    raise Http404

@login_required
def my_uploads(request):
    this_user = request.user
    files = file.objects.all()
    file_list = []
    print(this_user)
    for file_object in files:
        if file_object.username == this_user:
            print(file_object.username)
            print(file_object)
            file_list.append(file_object)

    return render(request, 'project/myuploads.html', {'file_list': file_list})



@login_required
def my_downloads(request):
    this_user = request.user
    downloaded_files = downloaded_file.objects.all()
    file_list = []
    for dl_file in downloaded_files:
        if dl_file.username == this_user:
            this_file = dl_file.file_downloaded
            file_list.append(this_file)

    return render(request, 'project/mydownloads.html', {'file_list': file_list})

def logout_view(request):
    logout(request)
    return redirect(index)

def aboutus(request):
    return render(request, 'project/aboutUS.html')


