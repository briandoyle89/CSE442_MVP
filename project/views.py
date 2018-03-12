# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from project.models import course, user, file
from .forms import *
import os
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'project/index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        for users in user.objects.all():
            if username == users.user_name and password == users.password:
                return redirect(course_list)
        return render(request, 'project/index.html', {'error_message': "Incorrect Username or Password."})
    return render(request, 'project/index.html')

def register(request):
    return render(request, 'project/register.html')


def check_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user.objects.create(user_name=username,
                            password=password,
                            email=email)
        for users in user.objects.all():
            print(users.user_name)
            print(users.password)
            print(users.email)
        return redirect(login)


def course_list(request):
    courses = course.objects.all()
    for course_ in courses: print(course_)
    user = request.user
    return render(request, 'project/dashboard.html', {'courses': courses})


def course_view(request, identity):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        files = file.objects.filter(course=course.objects.get(course_name=course_name))
        user = request.user
        return render(request, 'project/class_view.html', {'files': files,
                                                           'course_name': course_name})

def file_upload(request):

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            courses = course.objects.all()
            return render(request, 'project/dashboard.html', {'courses': courses})
    else:
        form = FileForm()
        return render(request, 'project/file_upload.html', {'form': form})



def download(request, file):
    file_path = settings.MEDIA_ROOT + '/' + file
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404